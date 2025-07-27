#!/usr/bin/env python3
import os

map_dir = "../map"

subdirs = [d for d in os.listdir(map_dir) if os.path.isdir(os.path.join(map_dir, d))]

missing_score = []
for d in sorted(subdirs):
    score_path = os.path.join(map_dir, d, "score")
    if not os.path.isfile(score_path) or os.path.getsize(score_path) <= 100:
        missing_score.append(d)

print(f"✅ 沒有有效 score 檔案（不存在或大小 ≤ 10 bytes）的資料夾總數：{len(missing_score)}")
for name in missing_score:
    print(name)

