import os
import numpy as np
import math

Rad=7.0
Div=0.375

def Gene_Grid():
  L_max=int(np.round(Rad/Div))
  L_min=-1*L_max
  grid=[]
  crd=[]
  for i in range (L_min,L_max+1):
    x=i*Div
    for j in range (L_min,L_max+1):
      y=j*Div
      for k in range (L_min,L_max+1):
        z=k*Div
        r=np.sqrt(x*x+y*y+z*z)
        if r<=Rad:
          grid.append(i)
          grid.append(j)
          grid.append(k)
          crd.append(x)
          crd.append(y)
          crd.append(z)
  gridn=np.array(grid).reshape(-1,3)
  crdn=np.array(crd).reshape(-1,3)
  return gridn,crdn

def Write_Grid(grid,crd):
  Type=["C"]
  fw1=open("Grid","w")
  fw2=open("Grid_type","w")
  ln=grid.shape[0]
  for i in range (ln):
    fw1.write("%3d %3d %3d %7.3f %7.3f %7.3f\n"%(grid[i][0],grid[i][1],grid[i][2],crd[i][0],crd[i][1],crd[i][2]))
  for i in range (len(Type)):
    for j in range (ln):
      fw2.write("%-2s %6d %3d %3d %3d\n"%(Type[i],i*ln+j,grid[j][0],grid[j][1],grid[j][2]))
  fw1.close()
  fw2.close()

def Main():
  grid,crd=Gene_Grid()
  Write_Grid(grid,crd)

Main()

