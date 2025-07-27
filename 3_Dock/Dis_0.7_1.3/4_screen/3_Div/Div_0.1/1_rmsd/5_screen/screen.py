import os
import numpy as np
import torch

Div=0.375

def Read_rmsd(pdb):
  fr=open("../4_superimpose/rmsd/%s"%(pdb),"r")
  rmsd=[]
  for line in fr:
    lx=line.split()
    if len(lx)==11:
      rmsd.append((float(lx[10]),int(lx[0]),int(lx[1]),int(lx[2]),int(lx[3]),float(lx[4]),
        float(lx[5]),float(lx[6]),float(lx[7]),float(lx[8]),float(lx[9])))
  fr.close()
  return sorted(rmsd)

def Main():
  pdb=sorted(os.listdir("../4_superimpose/rmsd"))
  for i in range (len(pdb)):
    fw=open("rmsd/%s"%(pdb[i]),"w")
    fw.write("                          Idx                     Trans                        Rotation               RMSD\n")
    rmsd=Read_rmsd(pdb[i])
    ln=len(rmsd)
    for m in range (ln):
      fw.write("%4s %3d %8d %5d %5d %5d   %8.3f %8.3f %8.3f   %9.4f %9.4f %9.4f   %7.4f\n"%(pdb[i][:4],m,rmsd[m][1],rmsd[m][2],
        rmsd[m][3],rmsd[m][4],rmsd[m][5],rmsd[m][6],rmsd[m][7],rmsd[m][8],rmsd[m][9],rmsd[m][10],rmsd[m][0]))
    fw.write("\n")
    fw.close()

Main()


