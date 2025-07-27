#!/usr/bin/env python3
import os
import re
import shutil

root_dir = "../1_map_score/1_prepare_gpf/map"
output_dir = "docked_pdbqt"
os.makedirs(output_dir, exist_ok=True)

summary = []

for folder in sorted(os.listdir(root_dir)):
    subdir = os.path.join(root_dir, folder)
    score_path = os.path.join(subdir, "score")
    num_path = os.path.join(subdir, "num")

    if not os.path.isfile(score_path) or not os.path.isfile(num_path):
        continue

    # 1. 搜尋所有包含能量值的行及其實際行號
    min_energy = None
    min_line_num = None

    with open(score_path) as f:
        for i, line in enumerate(f):
            match = re.search(r"= *([+-]?\d+\.\d+) kcal/mol", line)
            if match:
                energy = float(match.group(1))
                if (min_energy is None) or (energy < min_energy):
                    min_energy = energy
                    min_line_num = i  # 實際行號（從 0 開始）

    if min_line_num is None:
        continue

    # 2. 根據該行號，讀取 num 檔案中對應的 pdbqt 路徑
    with open(num_path) as f:
        num_lines = f.readlines()

    if min_line_num >= len(num_lines):
        continue

    num_line = num_lines[min_line_num]
    match = re.search(r'"([^"]+\.pdbqt)"', num_line)
    if not match:
        continue

    ligand_path = match.group(1)
    ligand_filename = os.path.basename(ligand_path)

    # 3. 複製 pdbqt 檔案
    if os.path.isfile(ligand_path):
        shutil.copy(ligand_path, os.path.join(output_dir, ligand_filename))

    # 4. 記錄 summary
    summary.append((folder, min_energy, ligand_filename))

# 5. 寫入 summary 結果
with open("Score", "w") as f:
    for folder, energy, filename in summary:
        f.write(f"{folder:<10s} {energy:10.2f}  {filename}\n")

