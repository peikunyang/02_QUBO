import os
import numpy as np
import math

def Read_Map(pdb):
  eg=[]
  fr=open("../../../1_CASF_2016/4_map/1_prepare_gpf/map/%s/%s_rec.C.map"%(pdb,pdb),"r")
  for line in fr:
    lx=line.split()
    if len(lx)==1:
      eg.append(float(lx[0]))
  fr.close()
  return np.array(eg).reshape(61,61,61).transpose(2,1,0)

def Write_Score(pdb,Map):
  fw=open("Map/%s.map"%(pdb),"w")
  fw.write("                      C\n")
  for i in range (61):
    for j in range (61):
      for k in range (61):
        fw.write("%3d %3d %3d"%(i-30,j-30,k-30))
        for m in range (len(Map)):
          fw.write(" %11.3f"%(Map[m][i][j][k]))
        fw.write("\n")
  fw.close()

def Main():
  pdb=sorted(os.listdir("../../1_grid/2_sel_lig_CASF/grid"))
  for i in range (len(pdb)):
    Map=[]
    name=pdb[i][:4]
    Map.append(Read_Map(name))
    Write_Score(name,Map)

Main()

