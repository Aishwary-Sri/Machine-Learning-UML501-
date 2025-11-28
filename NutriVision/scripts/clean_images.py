import os
import shutil
import pandas as pd

# ----------------------------
# MODIFY THESE PATHS IF NEEDED
# ----------------------------
metadata_path = r"D:\nutrition5k_dataset\metadata\dish_metadata.csv"
overhead_dir = r"D:\nutrition5k_dataset\imagery\realsense_overhead"
# ----------------------------

# Load valid dish IDs from metadata CSV
df = pd.read_csv(metadata_path)
valid_ids = set(df["dish_id"].astype(str))

print(f"Loaded {len(valid_ids)} valid dish_ids from metadata.")

# Scan overhead image directory
all_folders = os.listdir(overhead_dir)
deleted_count = 0

for folder in all_folders:
    folder_path = os.path.join(overhead_dir, folder)

    # Only act on directories
    if not os.path.isdir(folder_path):
        continue

    # Extract dish id (folder name must match dish_id)
    dish_id = folder.strip()

    # Delete if missing in metadata
    if dish_id not in valid_ids:
        shutil.rmtree(folder_path)
        deleted_count += 1
        print(f"Deleted folder: {folder_path}")

print(f"\nDone. Deleted {deleted_count} folders not present in metadata.")
