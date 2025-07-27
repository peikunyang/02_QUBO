import os
import numpy as np
import torch

Div=0.375

def Read_rmsd(pdb):
  fr=open("../5_screen/rmsd/%s"%(pdb),"r")
  lig=[]
  num=[]
  idx=[]
  tra=[]
  rot=[]
  for line in fr:
    lx=line.split()
    if len(lx)==13:
      lig.append(lx[0])
      num.append(int(lx[1]))
      for i in range (3,6):
        idx.append(int(lx[i]))
      for i in range (6,9):
        tra.append(float(lx[i]))
      for i in range (9,12):
        rot.append(float(lx[i]))
  fr.close()
  idxn=np.array(idx).reshape(-1,3)
  tran=np.array(tra).reshape(-1,3)
  rotn=np.array(rot).reshape(-1,3)
  return lig,num,idxn,tran,rotn

def Read_Lig_Crd(name):
  fr=open("../../../../../../../1_CASF_2016/6_Lig_database/4_rotation/crd/%s.crd"%(name[:4]))
  idx=[]
  crd=[]
  for line in fr:
    lx=line.split()
    idx.append(int(lx[0]))
    for i in range (1,4):
      crd.append(float(lx[i]))
  fr.close()
  crdn=torch.Tensor(crd).to(float).reshape(-1,3)
  return idx,crdn

def Read_Lig_X(name):
  crd=[]
  fr=open("../../../../1_X_crd/crd/%s"%(name[:4]),"r")
  for line in fr:
    lx=line.split()
    for i in range (1,4):
      crd.append(float(lx[i]))
  fr.close()
  crdn=torch.Tensor(crd).reshape(-1,3)
  return crdn

def Rot_Mat(alpha,beta,gamma):
  c1=np.cos(alpha)
  s1=np.sin(alpha)
  c2=np.cos(beta)
  s2=np.sin(beta)
  c3=np.cos(gamma)
  s3=np.sin(gamma)
  matrix=np.array([[c1*c3-c2*s1*s3,-c1*s3-c2*c3*s1,s1*s2],[c3*s1+c1*c2*s3,c1*c2*c3-s1*s3,-c1*s2],[s2*s3,c3*s2,c2]])
  return matrix

def Rot_forw(crd,tra,rot):
  crd2=np.transpose(np.matmul(Rot_Mat(rot[0],rot[1],rot[2]),np.transpose(crd-tra)))
  return crd2

def Rot_back(crd,tra,rot):
  crd2=np.transpose(np.matmul(Rot_Mat(-1*rot[2],-1*rot[1],-1*rot[0]),np.transpose(crd)))+tra
  return crd2

def Write_Crd(pdb,lig,num,idx,crd):
  fw=open("ligand/%s/%s_%d.crd"%(pdb,lig,num),"w")
  for i in range (crd.shape[0]):
    fw.write("%7d %8.3f %8.3f %8.3f\n"%(idx[i],crd[i][0],crd[i][1],crd[i][2]))
  fw.close()

def Main():
  pdb=sorted(os.listdir("../5_screen/rmsd"))
  for i in range (len(pdb)):
    lig_X=Read_Lig_X(pdb[i])
    lig,num,idx,tra,rot=Read_rmsd(pdb[i])
    isExist=os.path.exists("ligand/%s"%(pdb[i]))
    if not isExist:
      os.mkdir("ligand/%s"%(pdb[i]))
    for j in range (len(lig)):
      lig_idx,lig_coord=Read_Lig_Crd(lig[j])
      lig_coord2=Rot_back(lig_coord,tra[j],rot[j])
      Write_Crd(pdb[i],lig[j],num[j],lig_idx,lig_coord2)

Main()

