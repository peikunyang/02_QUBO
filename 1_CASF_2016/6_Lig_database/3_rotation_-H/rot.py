import os
import numpy as np
import math
import torch
from sklearn.preprocessing import normalize

def Read_Crd(name):
  Idx=[]
  crd=[]
  fr=open("../2_boundary_atoms/bound_atom/%s"%(name),"r")
  for line in fr:
    lx=line.split()
    Idx.append(int(lx[0]))
    for i in range (2,5):
      crd.append(float(lx[i]))
  fr.close()
  crdn=np.array(crd).reshape(-1,3)
  return Idx,crdn

def Center(Crd):
  crd=Crd-Crd[0]
  v1=np.cross(crd[1],crd[2])
  v2=v1/np.linalg.norm(v1)
  return crd,v2

def Rot_Mat(alpha,beta,gamma):
  c1=np.cos(alpha)
  s1=np.sin(alpha)
  c2=np.cos(beta)
  s2=np.sin(beta)
  c3=np.cos(gamma)
  s3=np.sin(gamma)
  matrix=np.array([[c1*c3-c2*s1*s3,-c1*s3-c2*c3*s1,s1*s2],[c3*s1+c1*c2*s3,c1*c2*c3-s1*s3,-c1*s2],[s2*s3,c3*s2,c2]])
  return matrix

def Rotation(Crd):
  Trans=Crd[0]
  Crd,V_nor=Center(Crd)
  alpha1=0
  beta1=np.arccos(V_nor[2])
  gamma1=np.arctan2(V_nor[0],V_nor[1])
  cd1=Crd[1]/np.linalg.norm(Crd[1])
  Crd2=np.transpose(np.matmul(Rot_Mat(alpha1,beta1,gamma1),np.transpose(Crd)))
  V_nor2=np.transpose(np.matmul(Rot_Mat(alpha1,beta1,gamma1),np.transpose(V_nor)))
  alpha2=np.arctan2(Crd2[1][0],Crd2[1][1])
  beta2=0
  gamma2=0
  Crd3=np.transpose(np.matmul(Rot_Mat(alpha2,beta2,gamma2),np.transpose(Crd2)))
  Ang=(alpha2,beta1,gamma1)
  return Crd3,Ang,Trans

def Rot_back(Crd,trans,ang):
  Crd2=np.transpose(np.matmul(Rot_Mat(-1*ang[2],-1*ang[1],-1*ang[0]),np.transpose(Crd)))+trans

def Write_Crd(name,idx,crd):
  fw=open("crd_-H/%s"%(name),"w")
  for i in range (crd.shape[0]):
    fw.write("%7d %8.3f %8.3f %8.3f\n"%(idx[i],crd[i][0],crd[i][1],crd[i][2]))
  fw.close()

def Write_Ang(name,ang,trans):
  fw=open("ligand_rot_angle","w")
  for i in range (len(name)):
    fw.write("%4s %8.3f %8.3f %8.3f %9.4f %9.4f %9.4f\n"%(name[i][:4],trans[i][0],trans[i][1],trans[i][2],ang[i][0],ang[i][1],ang[i][2]))
  fw.close()

def Main():
  X_name=sorted(os.listdir("../2_boundary_atoms/bound_atom"))
  Ang=[]
  Trans=[]
  for i in range (len(X_name)):
    name=X_name[i]
    Idx,Crd=Read_Crd(name)
    Crd2,ang,trans=Rotation(Crd)
    Ang.append(ang)
    Trans.append(trans)
    Write_Crd(name,Idx,Crd2)
  Write_Ang(X_name,Ang,Trans)

Main()



