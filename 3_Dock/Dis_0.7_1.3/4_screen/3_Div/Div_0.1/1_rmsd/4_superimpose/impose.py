import os
import numpy as np
import torch

Div=0.375
zero=torch.tensor(0.0000)
delta=torch.tensor(0.0001)

def Read_Crd(name):
  fr=open("../../../../../../../1_CASF_2016/6_Lig_database/3_rotation_-H/crd_-H/%s.crd"%(name[:4]))
  crd=[]
  for line in fr:
    lx=line.split()
    for i in range (1,4):
      crd.append(float(lx[i]))
  fr.close()
  crdn=torch.Tensor(crd).to(torch.float32).reshape(-1,3).to("cpu")
  return crdn

def Read_X(name):
  crd=[]
  fr=open("../../../../1_X_crd/crd/%s"%(name[:4]),"r")
  for line in fr:
    lx=line.split()
    for i in range (1,4):
      crd.append(float(lx[i]))
  fr.close()
  crdn=torch.Tensor(crd).to(torch.float32).reshape(-1,3)
  return crdn

def Read_Three(name):
  fr=open("../3_comp_dis/Index/%s"%(name))
  Ind=[]
  for line in fr:
    lx=line.split()
    Ind.append(int(lx[0]))
    Ind.append(int(lx[1]))
    Ind.append(int(lx[2]))
  Indn=np.array(Ind).reshape(-1,3)
  return Indn

def Rearrange(ind,crd):
  crd2=crd.repeat(ind.shape[0],1).reshape(ind.shape[0],crd.shape[0],crd.shape[1])
  crd3=crd2.clone()
  for i in range (ind.shape[0]):
    for j in range (3):
      crd3[i,[j,ind[i][j]],:]=crd3[i,[ind[i][j],j],:]
  del crd2
  return crd3.to("cpu")

def Center(Crd):
  crd2=Crd[:,0,:].reshape(Crd.shape[0],1,3)
  crd3=Crd-crd2
  v1=crd3[:,1,:]
  v2=crd3[:,2,:]
  v3=torch.cross(v1,v2)
  v3_norm=torch.norm(v3,dim=1)
  zero=torch.lt(v3_norm,delta)
  v3_norm2=(v3_norm+zero*delta).reshape(-1,1)
  v4=torch.div(v3,v3_norm2)
  del crd2,v1,v2,v3,zero,v3_norm2
  return crd3,v4

def Rot_Mat(alpha,beta,gamma):
  c1=torch.cos(alpha)
  s1=torch.sin(alpha)
  c2=torch.cos(beta)
  s2=torch.sin(beta)
  c3=torch.cos(gamma)
  s3=torch.sin(gamma)
  a11=(c1*c3-c2*s1*s3).reshape(-1,1)
  a12=(-c1*s3-c2*c3*s1).reshape(-1,1)
  a13=(s1*s2).reshape(-1,1)
  a21=(c3*s1+c1*c2*s3).reshape(-1,1)
  a22=(c1*c2*c3-s1*s3).reshape(-1,1)
  a23=(-c1*s2).reshape(-1,1)
  a31=(s2*s3).reshape(-1,1)
  a32=(c3*s2).reshape(-1,1)
  a33=(c2).reshape(-1,1)
  rot_mat=torch.cat((a11,a12,a13,a21,a22,a23,a31,a32,a33),1).reshape(-1,3,3)
  del c1,s1,c2,s2,c3,s3,a11,a12,a13,a21,a22,a23,a31,a32,a33
  return rot_mat

def Rotation(Crd):
  Trans=Crd[:,0,:]
  crd,V_nor=Center(Crd)
  alpha1=torch.zeros(crd.shape[0]).to("cpu")
  beta1=torch.acos(V_nor[:,2])
  gamma1=torch.atan2(V_nor[:,0],V_nor[:,1])
  crd2=torch.bmm(Rot_Mat(alpha1,beta1,gamma1),crd.permute(0,2,1)).permute(0,2,1)
  alpha2=torch.atan2(crd2[:,1,0],crd2[:,1,1])
  beta2=torch.zeros(Crd.shape[0]).to("cpu")
  gamma2=torch.zeros(Crd.shape[0]).to("cpu")
  crd3=torch.bmm(Rot_Mat(alpha2,beta2,gamma2),crd2.permute(0,2,1)).permute(0,2,1)
  Ang=(alpha2,beta1,gamma1)
  del crd,V_nor,alpha1,beta1,gamma1,crd2,alpha2,beta2,gamma2
  return crd3,Trans,Ang

def Superimpose(crd_X,crd_lig):
  crd_lig2=crd_lig.reshape(1,-1,3).expand(crd_X.shape[0],-1,3)
  D=torch.cdist(crd_lig2,crd_X,p=2.0,compute_mode="donot_use_mm_for_euclid_dist")
  D_min=torch.min(D,2)[0]
  rms=torch.sqrt(torch.mean(torch.square(D_min),1))
  del crd_lig2,D,D_min
  return rms

def Write_RMSD(pdb,ind,trans,ang,rmse):
  fw=open("rmsd/%s"%(pdb),"w")
  fw.write("                 Idx                     Trans                        Rotation               RMSD\n")
  for i in range (ind.shape[0]):
    fw.write("%8d %5d %5d %5d   %8.3f %8.3f %8.3f   %9.4f %9.4f %9.4f   %7.4f\n"
      %(i,ind[i][0],ind[i][1],ind[i][2],trans[i][0],trans[i][1],trans[i][2],ang[0][i],ang[1][i],ang[2][i],rmse[i]))
  fw.close()

def Main():
  pdb = sorted(os.listdir("../3_comp_dis/Index"))
  batch_size = 10000
  for i in range(len(pdb)):
    crd_X = Read_X(pdb[i])  # Read the coordinates of X grid
    Ind_X = Read_Three(pdb[i])  # The atoms (0,1,2) of ligand superimpose the index atoms of crd_X
    crd_lig = Read_Crd(pdb[i])  # The coordinates of ligand
    for start in range(0, Ind_X.shape[0], batch_size):
      end = min(start + batch_size, Ind_X.shape[0])
      Ind_X2 = Ind_X[start:end]
      crd_X2 = Rearrange(Ind_X2, crd_X)
      crd_X3, Trans, Ang = Rotation(crd_X2)
      rmse = Superimpose(crd_X3, crd_lig)
      if start == 0:
        fw = open("rmsd/%s" % pdb[i], "w")
        fw.write("                 Idx                     Trans                        Rotation               RMSD\n")
      else:
        fw = open("rmsd/%s" % pdb[i], "a")
      for j in range(Ind_X2.shape[0]):
        fw.write("%8d %5d %5d %5d   %8.3f %8.3f %8.3f   %9.4f %9.4f %9.4f   %7.4f\n" % (
            start + j,
            Ind_X2[j][0], Ind_X2[j][1], Ind_X2[j][2],
            Trans[j][0], Trans[j][1], Trans[j][2],
            Ang[0][j], Ang[1][j], Ang[2][j],
            rmse[j]
        ))
      fw.close()
      del Ind_X2, crd_X2, crd_X3, Trans, Ang, rmse
    del crd_lig, crd_X, Ind_X

Main()


