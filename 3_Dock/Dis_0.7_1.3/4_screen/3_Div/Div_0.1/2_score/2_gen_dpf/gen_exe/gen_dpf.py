import os,stat
import numpy as np
import shutil

def Write_dpf(pdb,ligt):
  lig=sorted(os.listdir("/mnt/SSD/kun/job/02_QUBO/1_rmsd/7_ligand_pdbqt/ligand/%s"%(pdb)))
  fw=open("../../1_map_score/1_prepare_gpf/map/%s/%s.dpf"%(pdb,pdb),"w")
  fw.write("autodock_parameter_version 4.2\n")
  fw.write("outlev ADT\n")
  fw.write("ligand_types")
  for i in range (len(ligt)):
    fw.write(" %s"%(ligt[i]))
  fw.write("\n")
  fw.write("fld %s_rec.maps.fld\n"%(pdb))
  for i in range (len(ligt)):
    fw.write("map %s_rec.%s.map\n"%(pdb,ligt[i]))
  fw.write("elecmap %s_rec.e.map\n"%(pdb))
  fw.write("dsolvmap %s_rec.d.map\n"%(pdb))
  for i in range (len(lig)): # len(lig)
    fw.write("move /mnt/SSD/kun/job/02_QUBO/1_rmsd/7_ligand_pdbqt/ligand/%s/%s\n"%(pdb,lig[i]))
    fw.write("epdb\n")
  fw.close()

def Search_Type(pdb):
  fr=open("../../1_map_score/1_prepare_gpf/map/%s/%s_ligand.pdbqt"%(pdb,pdb),"r")
  typ=[]
  for line in fr:
    if line[:4]=="ATOM":
      lx=line.split()
      typ.append(lx[len(lx)-1])
  set_type=sorted(list(set(typ)))
  fr.close()
  return set_type

def Main():
  pdb=sorted(os.listdir("../../1_map_score/1_prepare_gpf/map"))
  fw3=open("exe_score","w")
  os.chmod("exe_score",stat.S_IRWXU)
  for i in range (len(pdb)): 
    if (i%10==0):
      j=int(i/10)
      fw3.write("./exe_score_%d &\n"%(j))
      if i!=0:
        fw2.close()
      fw2=open("exe_score_%d"%(j),"w")
      os.chmod("exe_score_%d"%(j),stat.S_IRWXU)
    fw=open("../../1_map_score/1_prepare_gpf/map/%s/exe"%(pdb[i]),"w")
    os.chmod("../../1_map_score/1_prepare_gpf/map/%s/exe"%(pdb[i]),stat.S_IRWXU)
    Ty_lig=Search_Type("%s"%(pdb[i]))
    Write_dpf(pdb[i],Ty_lig)
    fw2.write("cd /mnt/SSD/kun/job/02_QUBO/2_score/1_map_score/1_prepare_gpf/map/%s\n"%(pdb[i]))
    fw.write("autodock4 -p %s.dpf -l %s.dlg\n"%(pdb[i],pdb[i]))
    fw2.write("./exe\n")
    fw2.write('grep "Ligand PDBQT file =" %s.dlg > num\n'%(pdb[i]))
    fw2.write('grep "epdb: USER    Estimated Free Energy of Binding    =" %s.dlg > score\n'%(pdb[i]))
    fw2.write("rm %s.dlg\n"%(pdb[i]))
    fw.close()
  fw2.close()
  fw3.close()

Main()


