import os
import numpy as np
import shutil

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

def RMSD_less(rmsd):
  count1=0
  count2=0
  count3=0
  count4=0
  for i in range (len(rmsd)):
    if rmsd[i]<2.0:
      count1=count1+1
    if rmsd[i]<1.5:
      count2=count2+1
    if rmsd[i]<1.0:
      count3=count3+1
    if rmsd[i]<0.6:
      count4=count4+1
  per1=100*count1/len(rmsd)
  per2=100*count2/len(rmsd)
  per3=100*count3/len(rmsd)
  per4=100*count4/len(rmsd)
  return per1,per2,per3,per4

def Write_RMSD(p1,len_pose,rmsd_min,rmsd_min_idx):
  fw=open("rmsd","w")
  rmsd=np.mean(rmsd_min)
  len_pose_ave=np.mean(np.array(len_pose))
  per1,per2,per3,per4=RMSD_less(rmsd_min)
  fw.write(" PDB %6.0f %6.2f %5.1f %5.1f %5.1f %5.1f\n"%(len_pose_ave,rmsd,per1,per2,per3,per4))
  for i in range (len(p1)):
    fw.write("%4s %6d %6.2f %6s\n"%(p1[i],len_pose[i],rmsd_min[i],rmsd_min_idx[i]))
  fw.close()

def Main():
  p1=sorted(os.listdir("/mnt/SSD/kun/job/02_QUBO/1_rmsd/7_ligand_pdbqt/ligand/"))
  len_pose=[]
  rmsd_min=[]
  rmsd_min_idx=[]
  for i in range (len(p1)):
    p2=sorted(os.listdir("/mnt/SSD/kun/job/02_QUBO/1_rmsd/7_ligand_pdbqt/ligand/%s"%(p1[i])))
    rmsd=[]
    cry_crd=Read_pdbqt("../../../../../../../1_CASF_2016/1_CASF_pdbqt/pdbqt/%s/%s_ligand.pdbqt"%(p1[i],p1[i]))
    for j in range (len(p2)):
      cubo_crd=Read_pdbqt("/mnt/SSD/kun/job/02_QUBO/1_rmsd/7_ligand_pdbqt/ligand/%s/%s"%(p1[i],p2[j]))
      rmsd.append(RMSD(cry_crd,cubo_crd))
    len_pose.append(len(p2))
    rmsd_min.append(np.min(np.array(rmsd)))
    lig_min=p2[np.argmin(np.array(rmsd))]
    rmsd_min_idx.append(lig_min)
    shutil.copyfile("/mnt/SSD/kun/job/02_QUBO/1_rmsd/7_ligand_pdbqt/ligand/%s/%s"%(p1[i],lig_min),"docked_pdbqt/%s"%(lig_min))
  Write_RMSD(p1,len_pose,rmsd_min,rmsd_min_idx)

Main()


