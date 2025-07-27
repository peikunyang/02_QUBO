#!/usr/bin/env python3
import pandas as pd

score_df = pd.read_csv("../../../../../../../../1_CASF_2016/7_score_exp/3_score/Score", delim_whitespace=True, header=None, usecols=[0, 1], names=["ID", "Score"])
rmsd_df = pd.read_csv("../../4_rmsd/Rmsd", delim_whitespace=True, header=None, usecols=[0, 1, 2], names=["File", "Rmsd1", "Rmsd2"])
rmsd_df["ID"] = rmsd_df["File"].str[:4]
merged_df = pd.merge(score_df, rmsd_df, on="ID", how="inner")
output_df = merged_df[["ID", "Score", "Rmsd1", "Rmsd2"]]
output_df.to_csv("Score", sep="\t", index=False, header=False)

