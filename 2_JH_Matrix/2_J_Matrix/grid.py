import os
import numpy as np
import math
import torch

Div=0.375
E_rep1 = torch.tensor(1, dtype=torch.int8)
E_bond = torch.tensor(-1, dtype=torch.int8)

def Read_Grid():
  fr=open("../1_grid/1_grid/Grid","r")
  crd=[]
  for line in fr:
    lx=line.split()
    crd.append(float(lx[3]))
    crd.append(float(lx[4]))
    crd.append(float(lx[5]))
  fr.close()
  crdT=torch.tensor(crd).reshape(-1,3)
  return crdT

def Read_Type():
  fr=open("Dis","r")
  dis=[]
  for line in fr:
    lx=line.split()
    dis.append((float(lx[0]),float(lx[1])))
  fr.close()
  return torch.tensor(dis).reshape(-1,2)

def Score_Grid(crd,disD):
  ln=crd.shape[0]
  D=torch.cdist(crd,crd,p=2.0,compute_mode="donot_use_mm_for_euclid_dist").reshape(ln,ln)
  for i in range (disD.shape[0]):
    fw=open("J_Matrix/Score_Bond_%3.1f_%3.1f"%(disD[i][0],disD[i][1]),"w")
    Bond_Score=torch.zeros((ln,ln),dtype=torch.int8)
    D1=torch.lt(D,torch.tensor(disD[i][0]))
    D2=torch.ge(D,torch.tensor(disD[i][0]))
    D3=torch.lt(D,torch.tensor(disD[i][1]))
    D4=torch.logical_and(D2,D3)
    Bond_Score=Bond_Score+E_rep1*D1+E_bond*D4
    del D1,D2,D3,D4
    Bond_Score=torch.triu(Bond_Score,diagonal=1)
    Write_Score(fw,Bond_Score)
    del Bond_Score
    fw.close()

def Write_Score(fw,D):
  DN=D.to("cpu").numpy()
  Idx=torch.nonzero(D,as_tuple=False).to("cpu").numpy()
  for i in range (Idx.shape[0]):
    m=Idx[i][0]
    n=Idx[i][1]
    fw.write("%d %d %2d\n"%(m,n,DN[m][n]))
  fw.flush()

def Main():
  Crd=Read_Grid()
  DisD=Read_Type()
  Score_Grid(Crd,DisD)

Main()

