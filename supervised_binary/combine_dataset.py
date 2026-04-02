import pandas as pd
import os
import time

# ---------- START TIMER ----------
start_time = time.time()

benign_file = "/home/bhavya-jain/Code/PBL/data/train/supervised_train_benign_clean.csv"
attack_folder = "/home/bhavya-jain/Code/PBL/data/train/attack_cleaned_binary_label"

# ---------- LOAD BENIGN ----------
print("Loading benign...")
benign = pd.read_csv(benign_file)
print(f"Benign loaded: {benign.shape}")

all_data = [benign]

# ---------- PROCESS ATTACK FILES ----------
files = [f for f in os.listdir(attack_folder) if f.endswith(".csv")]

print(f"\nTotal attack files: {len(files)}\n")

for i, file in enumerate(files, 1):
    path = os.path.join(attack_folder, file)

    t0 = time.time()

    df = pd.read_csv(path)
    all_data.append(df)

    t1 = time.time()

    print(f"[{i}/{len(files)}] Combined: {file} | Shape: {df.shape} | Time: {t1 - t0:.2f}s")

# ---------- COMBINE ----------
print("\nCombining all dataframes...")
combine_start = time.time()

final_df = pd.concat(all_data, ignore_index=True)

combine_end = time.time()

print("Final shape:", final_df.shape)
print(f"Concat time: {combine_end - combine_start:.2f}s")

# ---------- SAVE ----------
final_df.to_csv("/home/bhavya-jain/Code/PBL/data/train/binary_dataset.csv", index=False)

# ---------- TOTAL TIME ----------
end_time = time.time()

print("\nSaved: binary_dataset.csv")
print(f"Total execution time: {end_time - start_time:.2f}s")