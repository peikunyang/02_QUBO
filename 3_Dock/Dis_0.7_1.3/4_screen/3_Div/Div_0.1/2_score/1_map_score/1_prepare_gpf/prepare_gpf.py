import os
import numpy as np

def Write_gpf(pdb,rec,lig):
  fw=open("map/%s/%s.gpf"%(pdb,pdb),"w")
  fw.write("npts 60 60 60                        # num.grid points in xyz\n")
  fw.write("gridfld %s_rec.maps.fld            # grid_data_file\n"%(pdb))
  fw.write("spacing 0.375                        # spacing(A)\n")
  fw.write("receptor_types")
  for i in range (len(rec)):
    fw.write("%3s"%(rec[i]))
  fw.write("\n")
  fw.write("ligand_types")
  for i in range (len(lig)):
    fw.write("%3s"%(lig[i]))
  fw.write("\n")
  fw.write("receptor %s_protein.pdbqt          # macromolecule\n"%(pdb))
  fw.write("gridcenter 0 0 0                     # xyz-coordinates or auto\n")
  fw.write("smooth 0.5                           # store minimum energy w/in rad(A)\n")
  for i in range (len(lig)):
    fw.write("map %s_rec.%s.map                   # atom-specific affinity map\n"%(pdb,lig[i]))
  fw.write("elecmap %s_rec.e.map               # electrostatic potential map\n"%(pdb))
  fw.write("dsolvmap %s_rec.d.map              # desolvation potential map\n"%(pdb))
  fw.write("dielectric -0.1465                   # <0, AD4 distance-dep.diel;>0, constant\n")
  fw.close()

def Search_Type_Rec(pdb):
  fr=open("map/%s/%s_protein.pdbqt"%(pdb,pdb),"r")
  typ=[]
  for line in fr:
    if line[:4]=="ATOM":
      lx=line.split()
      typ.append(lx[len(lx)-1])
  set_type=list(set(typ))
  return set_type

def Search_Type_Lig(pdb):
  fr=open("map/%s/%s_ligand.pdbqt"%(pdb,pdb),"r")
  typ=[]
  for line in fr:
    if line[:4]=="ATOM":
      lx=line.split()
      typ.append(lx[len(lx)-1])
  set_type=list(set(typ))
  return set_type

def Main():
  pdb=sorted(os.listdir("map"))
  for i in range (len(pdb)):
    ty_rec=Search_Type_Rec(pdb[i])
    ty_lig=Search_Type_Lig(pdb[i])
    Write_gpf(pdb[i],ty_rec,ty_lig)

Main()


