import os
import numpy as np
import math
import shutil

def Read_Grid():
  fr=open("../1_grid/Grid","r")
  id2=[]
  for line in fr:
    lx=line.split()
    id1=(int(lx[0]),int(lx[1]),int(lx[2]))
    id2.append(id1)
  id3=set(id2)
  fr.close()
  return id2,id3

def Read_Lig(pdb):
  fr=open("../../2_grid/grid/%s_ligand"%(pdb),"r")
  ie2=[]
  for line in fr:
    lx=line.split()
    ie1=(int(lx[5]),int(lx[6]),int(lx[7]))
    ie2.append(ie1)
  ie3=set(ie2)
  fr.close()
  return ie2,ie3

def Write_Grid(name,ic2,ie4):
  fw=open("grid/%s.grid"%(name),"w")
  X=np.zeros(len(ic2))
  for i in range (len(ie4)):
    X[ic2.index(ie4[i])]=1
  for i in range (len(ic2)):
    fw.write("%d"%(X[i]))
  fw.write("\n")
  fw.close()

def Main():
  id2,id3=Read_Grid()
  pdb=sorted(os.listdir("../../2_grid/grid"))
  for i in range (len(pdb)):
    name=pdb[i][:4]
    ie2,ie3=Read_Lig(name)
    if1=ie3.difference(id3)
    if len(if1)==0:
      shutil.copyfile("../../2_grid/grid/%s_ligand"%(name),"crd/%s.crd"%(name))
      shutil.copytree("../../1_CASF_pdbqt/pdbqt/%s"%(name),"pdbqt/%s"%(name))
      Write_Grid(name,id2,ie2)

Main()


