import os
import numpy as np
import math
import torch

def Read_Rot():
  pdb=[]
  trans=[]
  rot=[]
  fr=open("../3_rotation_-H/ligand_rot_angle","r")
  for line in fr:
    lx=line.split()
    pdb.append(lx[0])
    for i in range (1,4):
      trans.append(float(lx[i]))
    for i in range (4,7):
      rot.append(float(lx[i]))
  fr.close()
  transn=np.array(trans).reshape(-1,3)
  rotn=np.array(rot).reshape(-1,3)
  return pdb,transn,rotn

def Read_Crd(name):
  Idx=[]
  crd=[]
  fr=open("../1_coord/coord/%s.crd"%(name),"r")
  for line in fr:
    lx=line.split()
    Idx.append(int(lx[0]))
    for i in range (2,5):
      crd.append(float(lx[i]))
  fr.close()
  crdn=np.array(crd).reshape(-1,3)
  return Idx,crdn

def Rot_Mat(alpha,beta,gamma):
  c1=np.cos(alpha)
  s1=np.sin(alpha)
  c2=np.cos(beta)
  s2=np.sin(beta)
  c3=np.cos(gamma)
  s3=np.sin(gamma)
  matrix=np.array([[c1*c3-c2*s1*s3,-c1*s3-c2*c3*s1,s1*s2],[c3*s1+c1*c2*s3,c1*c2*c3-s1*s3,-c1*s2],[s2*s3,c3*s2,c2]])
  return matrix

def Rotation(Crd,trans,ang):
  crd=Crd-trans
  alpha1=0
  beta1=ang[1]
  gamma1=ang[2]
  Crd2=np.transpose(np.matmul(Rot_Mat(alpha1,beta1,gamma1),np.transpose(crd)))
  alpha2=ang[0]
  beta2=0
  gamma2=0
  Crd3=np.transpose(np.matmul(Rot_Mat(alpha2,beta2,gamma2),np.transpose(Crd2)))
  return Crd3

def Write_Crd(name,idx,crd):
  fw=open("crd/%s.crd"%(name),"w")
  for i in range (crd.shape[0]):
    fw.write("%7d %8.3f %8.3f %8.3f\n"%(idx[i],crd[i][0],crd[i][1],crd[i][2]))
  fw.close()

def Main():
  pdb,trans,rot=Read_Rot()
  for i in range (len(pdb)):
    Idx,Crd=Read_Crd(pdb[i])
    Crd2=Rotation(Crd,trans[i],rot[i])
    Write_Crd(pdb[i],Idx,Crd2)

Main()



