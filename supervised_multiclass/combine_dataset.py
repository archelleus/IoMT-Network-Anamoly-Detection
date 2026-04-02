import pandas as pd
import os
import time

# ---------- PATHS ----------
benign_file = "/home/bhavya-jain/Code/PBL/data/train/multiclass_train_benign_clean.csv"
attack_folder = "/home/bhavya-jain/Code/PBL/data/train/multiclass_attack_cleaned"
output_file = "/home/bhavya-jain/Code/PBL/data/train/multiclass_dataset.csv"
# ---------------------------

start = time.time()

all_data = []

# ---------- BENIGN ----------
print("Loading benign...")
benign = pd.read_csv(benign_file)
print(f"Benign shape: {benign.shape}")

all_data.append(benign)

# ---------- ATTACK FILES ----------
files = [f for f in os.listdir(attack_folder) if f.endswith(".csv")]

print(f"\nFound {len(files)} attack files\n")

for i, file in enumerate(files, 1):
    t0 = time.time()

    path = os.path.join(attack_folder, file)
    df = pd.read_csv(path)

    all_data.append(df)

    t1 = time.time()
    print(f"[{i}/{len(files)}] {file} | {df.shape} | {t1 - t0:.2f}s")

# ---------- COMBINE ----------
print("\nCombining...")

combine_start = time.time()

final_df = pd.concat(all_data, ignore_index=True)

combine_end = time.time()

print("Final shape:", final_df.shape)
print(f"Concat time: {combine_end - combine_start:.2f}s")

# ---------- SAVE ----------
print("\nSaving...")

final_df.to_csv(output_file, index=False)

end = time.time()

print(f"\nSaved: {output_file}")
print(f"Total time: {end - start:.2f}s")