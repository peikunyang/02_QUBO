#!/usr/bin/env python3
import pandas as pd

def count_ratio(df, threshold):
    total = len(df)
    count = (df[3] < threshold).sum()
    ratio = count / total * 100 if total > 0 else 0
    return ratio

row1 = []
row2 = []

df_score = pd.read_csv("../1_comb/Score", delim_whitespace=True, header=None)
for t in [2.0, 1.5, 1.0]:
    r = count_ratio(df_score, t)
    row1.append(f"{r:.2f}")

for t in [2.0, 1.5, 1.0]:
    df_filtered = pd.read_csv(f"../2_less/Score_{t:.1f}", delim_whitespace=True, header=None)
    r = count_ratio(df_filtered, t)
    row2.append(f"{r:.2f}")

with open("per", "w") as f:
    f.write(" ".join(row1) + "\n")
    f.write(" ".join(row2) + "\n")


