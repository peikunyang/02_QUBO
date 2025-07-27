import os,sys,stat
import numpy as np
import math
import shutil

Div=0.375

def Lig_Coor(pdb):
  crd=[]
  chg=[]
  typ=[]
  fr=open("../1_CASF_pdbqt/pdbqt/%s/%s_ligand.pdbqt"%(pdb,pdb),"r")
  for line in fr:
    if line[:4]=="ATOM":
      crd.append(float(line[30:38]))
      crd.append(float(line[38:46]))
      crd.append(float(line[46:54]))
      chg.append(float(line[70:76]))
      typ.append(line[77:79])
  crdn=np.array(crd).reshape(-1,3)
  fr.close()
  return crdn,chg,typ

def Write_Data(pdb,Typ,Chg,Crd):
  CrdI=np.round(Crd/Div)
  fw=open("grid/%s_ligand"%(pdb),"w")
  for i in range (len(Typ)):
    if Typ[i][0]!="H":
      fw.write("%2s %6.3f %7.3f %7.3f %7.3f %3.0f %3.0f %3.0f\n"%(Typ[i],Chg[i],Crd[i][0],Crd[i][1],Crd[i][2],CrdI[i][0],CrdI[i][1],CrdI[i][2]))
  fw.close()

def Main():
  pdb=os.listdir("../1_CASF_pdbqt/pdbqt")
  for i in range (len(pdb)):
    Crd,Chg,Typ=Lig_Coor(pdb[i])
    Write_Data(pdb[i],Typ,Chg,Crd)

Main()

