import os
import csv
import shutil

# ====== ADJUST THIS FILE PATH ======
csv_path = r"D:\nutrition5k_dataset\metadata\dish_metadata_cafe2.csv"

# ====== ADJUST THIS DIRECTORY PATH ======
overhead_dir = r"D:\nutrition5k_dataset\imagery\realsense_overhead"

# Read dish_ids from CSV
dish_ids = []

with open(csv_path, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if row: 
            dish_id = row[0].strip()
            dish_ids.append(dish_id)

print(f"Found {len(dish_ids)} dish_ids in CSV.")

# Delete matching folders
deleted_count = 0

for dish_id in dish_ids:
    folder_path = os.path.join(overhead_dir, dish_id)

    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        deleted_count += 1
        print(f"Deleted folder: {folder_path}")
    else:
        print(f"Folder not found (skipped): {folder_path}")

print(f"\nCompleted. Total folders deleted: {deleted_count}")
