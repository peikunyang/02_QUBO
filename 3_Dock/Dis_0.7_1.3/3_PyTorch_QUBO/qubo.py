import os
import numpy as np
import math
import timeit
import torch
from torch import optim

learning_rate=1E-3 #1E-3
E_bond=-2
E_vdW=20
Num_Step=100000
pdb_Start=0
pdb_End=169

Num_X=27201
half=torch.tensor([0.5],dtype=float,device="cuda")
zero=torch.tensor([0.0],dtype=float,device="cuda")

def Grid():
  Id=[]
  fr=open("../../../2_JH_Matrix/1_grid/1_grid/Grid","r")
  for line in fr:
    lx=line.split()
    Id.append(int(lx[0]))
    Id.append(int(lx[1]))
    Id.append(int(lx[2]))
  Idn=np.array(Id).reshape(-1,3)
  fr.close()
  return Idn

def Read_J(Q):
  fr=open("../../../2_JH_Matrix/2_J_Matrix/J_Matrix/Score_Bond_0.7_1.3","r")
  for line in fr:
    lx=line.split()
    if int(lx[2])==1:
      s=E_vdW
    elif int(lx[2])==-1:
      s=E_bond
    else:
      print("Error: %s"%(line))
    Q[int(lx[0])][int(lx[1])]=s
  fr.close()
  return Q

def Read_H(name,Q):
  fr=open("../../../2_JH_Matrix/3_H_Matrix/2_grid_map/Map/%s.grid"%(name),"r")
  Vdw=[]
  for line in fr:
    lx=line.split()
    Vdw.append(float(lx[3]))
  fr.close()
  for i in range (len(Vdw)):
    Q[i][i]=Vdw[i]
  return Q

def Read_grid_crd(name):
  fr=open("../../../1_CASF_2016/3_less_7/2_sel_lig_CASF/crd/%s.crd"%(name),"r")
  Cr=[]
  Gr=[]
  for line in fr:
    lx=line.split()
    Cr.append(float(lx[2]))
    Cr.append(float(lx[3]))
    Cr.append(float(lx[4]))
    Gr.append(int(lx[5]))
    Gr.append(int(lx[6]))
    Gr.append(int(lx[7]))
  Crn=np.array(Cr).reshape(-1,3)
  Grn=np.array(Gr).reshape(-1,3)
  return Grn,Crn

def Convert_X(X):
  X2=torch.sigmoid(X.detach())
  X3=torch.heaviside(X2-half,zero)
  return X3

def Write_data(fw1,fw2,name,X,loss1,loss2):
  fw1.write("%4s "%(name))
  XB=Convert_X(X).to("cpu").numpy()
  for i in range (XB.shape[0]):
    fw1.write("%d"%(int(XB[i])))
  fw1.write("\n")

  fw1.write("\n")
  fw1.flush()

  fw2.write("%4s "%(name))
  for i in range (len(loss1)):
    fw2.write("%10.4f/%10.4f  "%(loss1[i],loss2[i]))
    if i%5==4:
      fw2.write("\n")
  if i%5!=4:
    fw2.write("\n")
  fw2.write("\n")
  fw2.flush()

def Train_X(Opt,Q,X):
  Opt.zero_grad()
  X2=torch.sigmoid(X).reshape(1,-1)
  X3=X2.reshape(-1,1)
  y1=torch.mm(X2,Q)
  loss=torch.mm(y1,X3)
  loss.backward()
  Opt.step()
  return X,loss

def Est_Score(X,Q):
  X1=Convert_X(X).reshape(1,-1)
  X2=X1.reshape(-1,1)
  y1=torch.mm(X1,Q)
  loss=torch.mm(y1,X2)
  return loss

def Score_to_Crd(X,Idn):
  Id_X=[]
  for i in range (X.shape[0]):
    if int(X[i])==1:
      Id_X.append(Idn[i][0])
      Id_X.append(Idn[i][1])
      Id_X.append(Idn[i][2])
  Id_Xn=np.array(Id_X).reshape(-1,3)
  return Id_Xn

def Com_xrd(fw,id_g,name,X):
  gr_l,cr_l=Read_grid_crd(name)
  gr_l=torch.from_numpy(gr_l).float()
  X2=Convert_X(X).to("cpu").numpy()
  id_X=Score_to_Crd(X2,id_g)
  if id_X.shape[0]>0:
    id_Xt=torch.from_numpy(id_X).float()
    D1=torch.cdist(gr_l,id_Xt,p=2.0,compute_mode="donot_use_mm_for_euclid_dist")
    D2=torch.min(D1,1)
    rmsd=torch.sqrt(torch.mean(D2[0]**2))
    fw.write("PDBID: %4s %4d %6.3f\n"%(name,id_X.shape[0],rmsd))
    fw.write("    solved         predicted\n")
    for i in range (len(D2[1])):
      a=D2[1][i].item()
      rd=D2[0][i].item()
      fw.write("%3d %3d %3d    %3d %3d %3d %4.1f\n"%(gr_l[i][0],gr_l[i][1],gr_l[i][2],id_X[a][0],id_X[a][1],id_X[a][2],rd))
    fw.flush()
  else:
    fw.write("PDBID: %4s %4d\n"%(name,id_X.shape[0]))

def Main():
  Idn_G=Grid()
  pdb=sorted(os.listdir("../../../1_CASF_2016/4_map/1_prepare_gpf/map"))
  Q=Read_J(np.zeros((Num_X,Num_X),dtype=float))
  fw1=open("Score/Xmat","w")
  fw2=open("Score/Scor","w")
  fw3=open("Score/Pred","w")
  for i in range (pdb_Start,pdb_End):
    X=torch.randn((Num_X),device="cuda",dtype=float,requires_grad=True)
    Opt=optim.SGD([X],lr=learning_rate,weight_decay=0.0,momentum=0.9)
    name=pdb[i][:4]
    Q2=torch.from_numpy(Read_H(name,Q)).to("cuda")
    Loss1=[]
    Loss2=[]
    for j in range (Num_Step):
      X,loss1=Train_X(Opt,Q2,X)
      if j%100==99:
        Loss1.append(loss1.detach().to("cpu").item())
        loss2=Est_Score(X,Q2)
        Loss2.append(loss2.to("cpu").item())
    Com_xrd(fw3,Idn_G,name,X.detach())
    del Q2
    Write_data(fw1,fw2,name,X,Loss1,Loss2)
  fw1.close()
  fw2.close()
  fw3.close()

Main()

