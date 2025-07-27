import os,sys,stat
import numpy as np
import math
import shutil

def Read_Casf():
  pdb=[]
  fr=open("affinity_CASF_2016","r")
  for line in fr:
    pdb.append(line[:4])
  fr.close()
  return pdb

def Main():
  pdb=Read_Casf()
  for i in range (len(pdb)):
    shutil.copytree("../../../2024/Annealer_program/Annealer_program/1_CASF_2016/1_CASF_pdbqt/pdbqt/%s"%(pdb[i]),"pdbqt/%s"%(pdb[i]))

Main()

