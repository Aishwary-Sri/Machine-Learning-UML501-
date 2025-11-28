import os
import csv

# -----------------------------
# MODIFY THESE PATHS IF NEEDED
# -----------------------------
train_path = r"D:\nutrition5k_dataset\dish_ids\splits\train.txt"
test_path = r"D:\nutrition5k_dataset\dish_ids\splits\test.txt"
metadata_folder = r"D:\nutrition5k_dataset\metadata\dish_metadata"
# -----------------------------


# Step 1: Load allowed dish_ids from train.txt and test.txt
allowed_ids = set()

def load_ids(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                dish_id = line.strip()
                if dish_id:
                    allowed_ids.add(dish_id)

load_ids(train_path)
load_ids(test_path)

print(f"Loaded {len(allowed_ids)} allowed dish_ids.")


# Step 2: Iterate through each metadata CSV file
for file in os.listdir(metadata_folder):
    if file.endswith(".csv"):
        csv_path = os.path.join(metadata_folder, file)
        print(f"\nProcessing: {csv_path}")

        # Read CSV content
        rows = []
        with open(csv_path, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # keep header
            for row in reader:
                if row and row[0] in allowed_ids:   # row[0] = dish_id
                    rows.append(row)

        print(f"Keeping {len(rows)} rows out of original {len(rows)}.")

        # Write filtered CSV back
        with open(csv_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)

print("\nMetadata cleaning complete!")
