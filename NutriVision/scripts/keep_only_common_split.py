#!/usr/bin/env python3
"""
make_common_splits.py

Produces:
 - D:\nutrition5k_dataset\dish_ids\splits\train.txt  (intersection of depth_train_ids & rgb_train_ids)
 - D:\nutrition5k_dataset\dish_ids\splits\test.txt   (intersection of depth_test_ids & rgb_test_ids)

Overwrite existing train.txt / test.txt.

Adjust the BASE_DIR variable below if your dataset is in a different location.
"""

import os

# ====== ADJUST THIS PATH IF YOUR DATASET IS LOCATED ELSEWHERE ======
BASE_DIR = r"D:\nutrition5k_dataset\dish_ids\splits"
# ==================================================================

files = {
    "depth_train": os.path.join(BASE_DIR, "depth_train_ids.txt"),
    "rgb_train":   os.path.join(BASE_DIR, "rgb_train_ids.txt"),
    "depth_test":  os.path.join(BASE_DIR, "depth_test_ids.txt"),
    "rgb_test":    os.path.join(BASE_DIR, "rgb_test_ids.txt"),
}

def read_ids(path):
    if not os.path.isfile(path):
        print(f"Warning: file not found: {path}")
        return set()
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    # filter out empty lines and possible comments
    ids = set([l for l in lines if l and not l.startswith("#")])
    return ids

def write_ids(path, ids):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for d in sorted(ids):
            f.write(d + "\n")
    print(f"Wrote {len(ids)} ids to {path}")

def main():
    depth_train = read_ids(files["depth_train"])
    rgb_train   = read_ids(files["rgb_train"])
    depth_test  = read_ids(files["depth_test"])
    rgb_test    = read_ids(files["rgb_test"])

    common_train = depth_train.intersection(rgb_train)
    common_test  = depth_test.intersection(rgb_test)

    out_train = os.path.join(BASE_DIR, "train.txt")
    out_test  = os.path.join(BASE_DIR, "test.txt")

    write_ids(out_train, common_train)
    write_ids(out_test, common_test)

    print("Done.")
    print(f"Common train ids: {len(common_train)}")
    print(f"Common test ids : {len(common_test)}")

if __name__ == "__main__":
    main()
