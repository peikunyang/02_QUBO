#!/usr/bin/env python3
import pandas as pd

df = pd.read_csv("../1_comb/Score", delim_whitespace=True, header=None,
                 names=["ID", "Score", "Rmsd1", "Rmsd2"])

for t in [2.0, 1.5, 1.0]:
    out = df[~((df[["Rmsd2"]].values > t) & (df[["Rmsd1"]].values < df[["Score"]].values)).flatten()]
    out.to_csv(f"Score_{t:.1f}", sep="\t", index=False, header=False, float_format="%.2f")

