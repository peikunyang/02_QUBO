import os
import numpy as np
import math

def Grid():
  Id=[]
  fr=open("../../1_grid/1_grid/Grid","r")
  for line in fr:
    lx=line.split()
    Id.append(int(lx[0]))
    Id.append(int(lx[1]))
    Id.append(int(lx[2]))
  Idn=np.array(Id).reshape(-1,3)
  return Idn

def Read_Map(pdb):
  grid=[]
  vdw=[]
  fr=open("../1_map_sum/Map/%s.map"%(pdb),"r")
  for line in fr:
    lx=line.split()
    if len(lx)==4:
      grid.append(int(lx[0]))
      grid.append(int(lx[1]))
      grid.append(int(lx[2]))
      vdw.append(float(lx[3]))
  fr.close()
  gridn=np.array(grid).reshape(61,61,61,3)
  vdwn=np.array(vdw).reshape(61,61,61)
  return gridn,vdwn

def Write_Grid(pdb,Id,grid_pdbqt,vdw):
  fw=open("Map/%s.grid"%(pdb),"w")
  for i in range (Id.shape[0]):
    x=Id[i][0]+30
    y=Id[i][1]+30
    z=Id[i][2]+30
    score=vdw[x][y][z]
    fw.write("%3d %3d %3d %11.3f\n"%(Id[i][0],Id[i][1],Id[i][2],score))
  fw.close()

def Main():
  Id=Grid()
  pdb=sorted(os.listdir("../1_map_sum/Map"))
  for i in range (len(pdb)):
    name=pdb[i][:4]
    grid_pdbqt,vdw=Read_Map(name)
    Write_Grid(name,Id,grid_pdbqt,vdw)

Main()

