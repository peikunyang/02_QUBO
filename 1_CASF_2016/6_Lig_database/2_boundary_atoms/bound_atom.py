import os
import numpy as np
import math
import torch

def Read_Crd(name):
  crd=[]
  atom=[]
  fr=open("../1_coord/coord_-H/%s"%(name),"r")
  for line in fr:
    atom.append(line)
    lx=line.split()
    for i in range (2,5):
      crd.append(float(lx[i]))
  fr.close()
  crdn=torch.Tensor(crd).reshape(-1,3)
  return crdn,atom

def Dist(crd):
  ln=crd.shape[0]
  D=torch.cdist(crd,crd,p=2.0,compute_mode="donot_use_mm_for_euclid_dist")
  Dmax0=torch.max(D,1)
  Dmax1=torch.max(Dmax0[0],0)
  xi=Dmax1[1].item()
  yi=Dmax0[1][xi].item()
  zi=-1
  kmax=-1
  for i in range (ln):
    if ((i!=xi)&(i!=yi)):
      z0=D[xi,i].item()
      z1=D[i,yi].item()
      z2=z0+z1
      if kmax<z2:
        kmax=z2
        zi=i
  z0=D[xi,zi].item()
  z1=D[zi,yi].item()
  if z0>z1:
    Idx=[xi,yi,zi]
    Dis=[D[xi,yi].item(),D[xi,zi].item(),D[yi,zi].item()]
  else:
    Idx=[yi,xi,zi]
    Dis=[D[xi,yi].item(),D[yi,zi].item(),D[xi,zi].item()]
  return Idx,Dis

def Write_Crd(name,atom,idx):
  fw=open("bound_atom/%s.crd"%(name),"w")
  for i in range (3):
    j=idx[i]
    fw.write("%s"%(atom[j]))
  for i in range (len(atom)):
    if ((i!=idx[0])&(i!=idx[1])&(i!=idx[2])):
      fw.write("%s"%(atom[i]))
  fw.close()

def Write_Dis(name,dis):
  fw=open("dis/%s.dis"%(name),"w")
  fw.write("%8.5f %8.5f %8.5f\n"%(dis[0],dis[1],dis[2]))
  fw.close()

def Main():
  Lig_name=sorted(os.listdir("../1_coord/coord_-H"))
  for i in range (len(Lig_name)):
    name=Lig_name[i]
    Crd,Atom=Read_Crd(name)
    Idx,Dis=Dist(Crd)
    Write_Crd(name[:4],Atom,Idx)
    Write_Dis(name[:4],Dis)

Main()


