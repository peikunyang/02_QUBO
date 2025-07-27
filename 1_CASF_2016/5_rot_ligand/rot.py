import os
import numpy as np
import torch

def Read_Crd(name):
  fr=open("../4_map/1_prepare_gpf/map/%s/%s_ligand.pdbqt"%(name,name))
  pdbqt=[]
  crd=[]
  for line in fr:
    pdbqt.append(line)
    if line[:4]=="ATOM":
      lx=line.split()
      for i in range (5,8):
        crd.append(float(lx[i]))
  fr.close()
  crdn=torch.Tensor(crd).reshape(-1,3).transpose(0,1)
  return pdbqt,crdn

def Trans(crd):
  del_tran=10*torch.rand(3,1)
  crd=crd+del_tran
  return crd

def Rot_Mat(alpha,beta,gamma):
  c1=torch.cos(alpha)
  s1=torch.sin(alpha)
  c2=torch.cos(beta)
  s2=torch.sin(beta)
  c3=torch.cos(gamma)
  s3=torch.sin(gamma)
  a11=(c1*c3-c2*s1*s3).reshape(-1,1)
  a12=(-c1*s3-c2*c3*s1).reshape(-1,1)
  a13=(s1*s2).reshape(-1,1)
  a21=(c3*s1+c1*c2*s3).reshape(-1,1)
  a22=(c1*c2*c3-s1*s3).reshape(-1,1)
  a23=(-c1*s2).reshape(-1,1)
  a31=(s2*s3).reshape(-1,1)
  a32=(c3*s2).reshape(-1,1)
  a33=(c2).reshape(-1,1)
  rot_mat=torch.cat((a11,a12,a13,a21,a22,a23,a31,a32,a33),1).reshape(3,3)
  return rot_mat

def Rotation(crd):
  alpha=2.0*torch.pi*torch.rand(1)
  beta=torch.pi*torch.rand(1)
  gamma=2.0*torch.pi*torch.rand(1)
  crd2=torch.mm(Rot_Mat(alpha,beta,gamma),crd)
  return crd2

def Write_pdbqt(lig,pdbqt,crd):
  fw=open("ligand_pdbqt/%s_ligand.pdbqt"%(lig),"w")
  for i in range (len(pdbqt)):
    if pdbqt[i][:4]=="ATOM":
      m=int(pdbqt[i][4:11])-1
      fw.write("%s%8.3f%8.3f%8.3f%s"%(pdbqt[i][:30],crd[m][0],crd[m][1],crd[m][2],pdbqt[i][54:]))
    else:
      fw.write("%s"%(pdbqt[i]))
  fw.close()

def Main():
  lig=sorted(os.listdir("../4_map/1_prepare_gpf/map"))
  for i in range (len(lig)):
    pdbqt,crdn=Read_Crd(lig[i])
    for j in range (5):
      crd2=Trans(crdn)
      crdn=Rotation(crd2)
    Write_pdbqt(lig[i],pdbqt,crdn.transpose(0,1))

Main()

