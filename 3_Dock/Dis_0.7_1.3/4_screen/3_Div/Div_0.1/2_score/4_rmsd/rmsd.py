import os
import numpy as np
import shutil

def Read_score():
  fr=open("../3_score/Score","r")
  name=[]
  score=[]
  for line in fr:
    lx=line.split()
    name.append(lx[2])
    score.append(float(lx[1]))
  fr.close()
  return name,score

def Read_pdbqt(path):
  fr=open("%s"%(path),"r")
  crd=[]
  for line in fr:
    if line[:4]=="ATOM":
      crd.append(float(line[30:38]))
      crd.append(float(line[38:46]))
      crd.append(float(line[46:54]))
  crdn=np.array(crd).reshape(-1,3)
  fr.close()
  return crdn

def RMSD(cry,cubo):
  diff=cry-cubo
  diff2=diff*diff
  diff3=np.sqrt(diff2.sum(axis=1).mean())
  return diff3

def Write_RMSD(name,score,rmsd):
  fw=open("Rmsd","w")
  for i in range (len(name)):
    fw.write("%-20s %10.2f %10.2f\n"%(name[i],score[i],rmsd[i]))
  fw.close()

def Main():
  rmsd=[]
  name,score=Read_score()
  for i in range (len(name)):
    cry_crd=Read_pdbqt("/home/kun/job/02_QUBO/2025_06_05/1_CASF_2016/1_CASF_pdbqt/pdbqt/%s/%s_ligand.pdbqt"%(name[i][:4],name[i][:4]))
    cubo_crd=Read_pdbqt("../3_score/docked_pdbqt/%s"%(name[i]))
    rmsd.append(RMSD(cry_crd,cubo_crd))
  Write_RMSD(name,score,rmsd)

Main()


