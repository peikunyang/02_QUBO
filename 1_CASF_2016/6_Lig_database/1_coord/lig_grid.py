import os
import numpy as np
import math

Div=0.375

def Read_pdbqt(name):
  Crd=[]
  fr=open("../../5_rot_ligand/ligand_pdbqt/%s_ligand.pdbqt"%(name),"r")
  for line in fr:
    if line[:4]=="ATOM":
      lx=line.split()
      idx=int(lx[1])
      T=lx[len(lx)-1]
      x=float(line[30:38])
      y=float(line[38:46])
      z=float(line[46:54])
      Crd.append((idx,T,x,y,z))
  fr.close()
  return Crd

def Write_Crd(name,Crd):
  fw1=open("coord/%s.crd"%(name),"w")
  fw2=open("coord_-H/%s.crd"%(name),"w")
  for i in range (len(Crd)):
    x=float(Crd[i][2])
    y=float(Crd[i][3])
    z=float(Crd[i][4])
    fw1.write("%7d %-2s %8.3f %8.3f %8.3f\n"%(Crd[i][0],Crd[i][1],x,y,z))
    if ((Crd[i][1][0]!="H")&(Crd[i][1][0]!="HD")):
      fw2.write("%7d %-2s %8.3f %8.3f %8.3f\n"%(Crd[i][0],Crd[i][1],x,y,z))
  fw1.close()
  fw2.close()

def Main():
  Lig_name=sorted(os.listdir("../../5_rot_ligand/ligand_pdbqt"))
  for i in range (len(Lig_name)):
    name=Lig_name[i][:4]
    Crd=Read_pdbqt(name)
    Write_Crd(name,Crd)

Main()

