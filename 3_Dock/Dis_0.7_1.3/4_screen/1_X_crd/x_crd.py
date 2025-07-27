import os
import numpy as np
import math
import shutil
import torch

Div=0.375

def Grid():
  Id=[]
  fr=open("../../../../2_JH_Matrix/1_grid/1_grid/Grid_1_type","r")
  for line in fr:
    lx=line.split()
    Id.append((lx[0],int(lx[2]),int(lx[3]),int(lx[4])))
  fr.close()
  return Id

def Read_Score():
  name=[]
  X=[]
  fr=open("../../3_PyTorch_QUBO/Score/Xmat","r")
  for line in fr:
    lx=line.split()
    if len(lx)==2:
      name.append(lx[0])
      X.append(lx[1])
  fr.close()
  return name,X

def Con_Score_Id(Id_database,X):
  Tp=[]
  Id=[]
  for i in range (len(X)):
    if X[i]=="1":
      Tp.append(Id_database[i][0])
      Id.append(Id_database[i][1])
      Id.append(Id_database[i][2])
      Id.append(Id_database[i][3])
  Idn=np.array(Id).reshape(-1,3)
  return Tp,Idn

def Write_Crd(name,Tp,Id):
  fw=open("crd/%s"%(name),"w")
  for i in range (len(Tp)):
    x=Id[i][0]*Div
    y=Id[i][1]*Div
    z=Id[i][2]*Div
    fw.write("%-2s %8.3f %8.3f %8.3f\n"%(Tp[i],x,y,z))
  fw.close()

def Write_Num_Atm(pdb,count):
  fw=open("Num_atom","w")
  ave=np.mean(np.array(count))
  fw.write("     %8.0f\n"%(ave))
  for i in range (len(pdb)):
    fw.write("%4s %8d\n"%(pdb[i],count[i]))
  fw.close()

def Main():
  Idg=Grid()
  pdb,X=Read_Score()
  count=[]
  for i in range (len(pdb)):
    Tp,Id=Con_Score_Id(Idg,X[i])
    count.append(X[i].count("1"))
    if len(Tp)>=20:
      Write_Crd(pdb[i],Tp,Id)
    else:
      print(pdb[i])
  Write_Num_Atm(pdb,count)

Main()

