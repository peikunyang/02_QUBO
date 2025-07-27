import os
import numpy as np
import torch

Div=0.375
Div_Err=0.1*Div

def X_coord(name):
  fr=open("../../../../2_distance/crd_dis/%s"%(name))
  dist=[]
  for line in fr:
    lx=line.split()
    ln=len(lx)
    for j in range (ln):
      dist.append(float(lx[j]))
  distn=torch.tensor(dist).to("cpu").reshape(ln,ln)
  return distn

def Read_Dis(name):
  fr=open("../../../../../../../1_CASF_2016/6_Lig_database/2_boundary_atoms/dis/%s"%(name))
  for line in fr:
    lx=line.split()
    dist=[float(lx[0]),float(lx[1]),float(lx[2])]
  return torch.tensor(dist).to("cpu").to(torch.float)

def Index(Lig_X,dist):
  D1=Lig_X-dist
  D2=torch.abs(D1)
  D3=torch.le(D2,torch.tensor(Div_Err))
  D4=torch.nonzero(D3)
  return D3.to("cpu"),D4.to("cpu")

def Search(Lig_X,dist):
  D0,Idx0=Index(Lig_X,dist[0])
  D1,Idx1=Index(Lig_X,dist[1])
  D2,Idx2=Index(Lig_X,dist[2])
  n1=D0.shape[0]
  n2=Idx0.shape[0]
  ik_mat=torch.zeros(n2,n1,dtype=torch.bool)
  kj_mat=torch.zeros(n2,n1,dtype=torch.bool)
  for i in range (n2):
    ik_mat[i,:]=D1[Idx0[i][0],:]
    kj_mat[i,:]=D2.permute(1,0)[Idx0[i][1],:]
  E1=torch.logical_and(ik_mat,kj_mat)
  E2=torch.nonzero(E1)
  Idx=[]
  for i in range (E2.shape[0]):
    Idx.append([Idx0[E2[i][0]][0],Idx0[E2[i][0]][1],E2[i][1]])
  return torch.tensor(Idx)

def Comp(Idx_X,Lig_X,dist):
  dis_X=[]
  for i in range (Idx_X.shape[0]):
    xi=Idx_X[i][0]
    xj=Idx_X[i][1]
    xk=Idx_X[i][2]
    dis_X.append([Lig_X[xi,xj],Lig_X[xi,xk],Lig_X[xj,xk]])
  D=torch.cdist(torch.tensor(dis_X).to("cpu").reshape(-1,3),dist.reshape(1,3).to("cpu"),p=2.0,compute_mode="donot_use_mm_for_euclid_dist").reshape(-1)
  D2=D.sort()
  return D2[0].to("cpu"),D2[1].to("cpu")

def Write_Idx(lig_dis,Lig_X,idx_rmsd,rmsd,Idx_X):
  fw=open("Index/%s"%(lig_dis),"w")
  num=rmsd.shape[0]
  for i in range (num):
    j=idx_rmsd[i]
    xi=Idx_X[j][0]
    xj=Idx_X[j][1]
    xk=Idx_X[j][2]
    dij=Lig_X[xi,xj]
    dik=Lig_X[xi,xk]
    djk=Lig_X[xj,xk]
    fw.write("%5d %5d %5d %6.3f %6.3f %6.3f %6.3f\n"%(xi,xj,xk,dij,dik,djk,rmsd[i]))
  fw.close()

def Main():
  X_name=sorted(os.listdir("../../../../2_distance/crd_dis"))
  for i in range (len(X_name)):
    Lig_X=X_coord(X_name[i])
    dist=Read_Dis(X_name[i])
    Idx_X=Search(Lig_X,dist)
    rmsd,idx_rmsd=Comp(Idx_X,Lig_X,dist)
    if len(idx_rmsd)>0:
      Write_Idx(X_name[i][:4],Lig_X,idx_rmsd,rmsd,Idx_X)

Main()

