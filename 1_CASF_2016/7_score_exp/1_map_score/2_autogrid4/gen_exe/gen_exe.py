import os
import numpy as np

def Main():
  pdb=sorted(os.listdir("../../1_prepare_gpf/map"))
  fw2=open("exe_exe","w")
  for i in range (len(pdb)):
    if i%20==0:
      m=int(np.round(i/20))
      if i!=0:
        fw.close()
      fw=open("exe_%d"%(m),"w")
      fw2.write("./exe_%d &\n"%(m))
    fw.write("cd /home/kun/job/02_QUBO/2025_06_05/4_Ana/1_dock/1_map_score/1_prepare_gpf/map/%s\n"%(pdb[i]))
    fw.write("autogrid4 -p %s.gpf -l %s.dlg\n"%(pdb[i],pdb[i]))
  fw.close()
  fw2.close()

Main()


