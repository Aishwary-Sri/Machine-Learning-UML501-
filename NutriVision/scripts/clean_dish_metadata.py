# filter_overwrite_dish_metadata.py
import pandas as pd
from pathlib import Path

# ======= EDIT THESE PATHS IF NEEDED ========
PATH_METADATA = Path(r"D:\nutrition5k_dataset\metadata\dish_metadata.csv")
PATH_SIDE_IMAGERY = Path(r"D:\nutrition5k_dataset\imagery\realsense_overhead")
PATH_SPLITS_DIR = Path(r"D:\nutrition5k_dataset\dish_ids\splits")
# ===========================================

# checks
if not PATH_METADATA.exists():
    raise FileNotFoundError(f"Metadata file not found: {PATH_METADATA}")
if not PATH_SIDE_IMAGERY.exists() or not PATH_SIDE_IMAGERY.is_dir():
    raise FileNotFoundError(f"Imagery folder not found: {PATH_SIDE_IMAGERY}")
if not PATH_SPLITS_DIR.exists():
    raise FileNotFoundError(f"Splits folder not found: {PATH_SPLITS_DIR}")

# read metadata
df = pd.read_csv(PATH_METADATA, dtype=str)  # read as strings to preserve ids
orig_count = len(df)
print(f"Loaded metadata: {orig_count} rows")

# normalize dish_id column name: find the column that contains 'dish' and 'id'
dish_col = None
for c in df.columns:
    if c.lower() == "dish_id" or c.lower() == "dishid" or "dish" in c.lower() and "id" in c.lower():
        dish_col = c
        break
if dish_col is None:
    # fallback: assume first column is dish id
    dish_col = df.columns[0]
    print(f"Warning: could not find explicit 'dish_id' column name. Using first column: '{dish_col}'")

# ensure dish_id column has no surrounding whitespace
df[dish_col] = df[dish_col].astype(str).str.strip()

# collect dish ids from imagery folder (subdirectory names)
imagery_ids = {p.name for p in PATH_SIDE_IMAGERY.iterdir() if p.is_dir()}
print(f"Found {len(imagery_ids)} dish folders in imagery (realsense_overhead)")

# read train/test split files and union them
depth_train = PATH_SPLITS_DIR / "depth_train_ids.txt"
depth_test  = PATH_SPLITS_DIR / "depth_test_ids.txt"
rgb_train   = PATH_SPLITS_DIR / "rgb_train_ids.txt"
rgb_test    = PATH_SPLITS_DIR / "rgb_test_ids.txt"

split_files = [depth_train, depth_test, rgb_train, rgb_test]
split_ids = set()
for f in split_files:
    if f.exists():
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                s = line.strip()
                if s:
                    split_ids.add(s)
    else:
        print(f"Warning: split file not found (skipping): {f}")

print(f"Collected {len(split_ids)} dish ids from split files (union of train/test)")

# target keep set: present in imagery AND present in split union
keep_ids = {did for did in imagery_ids if did in split_ids}
print(f"Intersection set (imagery ∩ splits): {len(keep_ids)} dish ids will be kept")

# filter dataframe: keep only rows whose dish_id is in keep_ids
before_filter = len(df)
df_filtered = df[df[dish_col].isin(keep_ids)].copy()
after_filter = len(df_filtered)
print(f"Rows before filter: {before_filter}, after filtering by presence: {after_filter}")

# drop duplicate dish_id rows (keep first)
before_dedup = len(df_filtered)
df_filtered = df_filtered.drop_duplicates(subset=[dish_col], keep="first")
after_dedup = len(df_filtered)
duplicates_dropped = before_dedup - after_dedup
print(f"Duplicates dropped: {duplicates_dropped}. Rows now: {after_dedup}")

# overwrite the original CSV (no backup)
df_filtered.to_csv(PATH_METADATA, index=False)
print(f"Overwrote original metadata file at: {PATH_METADATA}")
print("Done.")

