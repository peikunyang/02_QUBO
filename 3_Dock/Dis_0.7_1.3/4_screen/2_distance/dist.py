import os
import numpy as np
import math
import torch

def Read_Crd(name):
  crd=[]
  fr=open("../1_X_crd/crd/%s"%(name),"r") 
  for line in fr:
    lx=line.split()
    for i in range (1,4):
      crd.append(float(lx[i]))
  fr.close()
  crdn=torch.Tensor(crd).reshape(-1,3)
  return crdn

def Write_Crd(name,crd):
  D=torch.cdist(crd,crd,p=2.0,compute_mode="donot_use_mm_for_euclid_dist").numpy()
  fw=open("crd_dis/%s.dis"%(name),"w")
  for i in range (D.shape[0]):
    for j in range (D.shape[1]):
      fw.write("%7.4f "%(D[i][j]))
    fw.write("\n")
  fw.close()

def Main():
  lig_name=sorted(os.listdir("../1_X_crd/crd"))
  for j in range (len(lig_name)):
    name=lig_name[j]
    Crd=Read_Crd(name)
    Write_Crd(name[:4],Crd)

Main()


