import csv
import os

# ====== FILE PATHS (EDIT THESE IF YOUR PATHS DIFFER) ======
metadata_csv = r"D:\nutrition5k_dataset\metadata\dish_metadata_cafe2.csv"

depth_test   = r"D:\nutrition5k_dataset\dish_ids\splits\depth_test_ids.txt"
depth_train  = r"D:\nutrition5k_dataset\dish_ids\splits\depth_train_ids.txt"
rgb_test     = r"D:\nutrition5k_dataset\dish_ids\splits\rgb_test_ids.txt"
rgb_train    = r"D:\nutrition5k_dataset\dish_ids\splits\rgb_train_ids.txt"

split_files = [depth_test, depth_train, rgb_test, rgb_train]

# ====== STEP 1: LOAD dish_ids from CSV ======
dish_ids_to_delete = set()

with open(metadata_csv, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        dish_id = row[0].strip()
        if dish_id:
            dish_ids_to_delete.add(dish_id)

print(f"Loaded {len(dish_ids_to_delete)} dish_ids to remove.\n")

# ====== STEP 2: REMOVE dish_ids FROM EACH SPLIT FILE ======
for file_path in split_files:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    # Read existing IDs
    with open(file_path, "r") as f:
        ids = [line.strip() for line in f.readlines()]

    # Filter out unwanted IDs
    new_ids = [i for i in ids if i not in dish_ids_to_delete]

    # Write back filtered list
    with open(file_path, "w") as f:
        for id_ in new_ids:
            f.write(id_ + "\n")

    print(f"Updated: {file_path}")
    print(f"  Removed {len(ids) - len(new_ids)} dish_id records.\n")

print("✔ All split files updated successfully.")
