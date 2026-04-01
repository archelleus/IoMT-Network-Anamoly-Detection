import pandas as pd
import os

# ---------- PATHS ----------
benign_file = "/home/bhavya-jain/Code/PBL/data/train/supervised_train_benign_clean.csv"
attack_folder = "/home/bhavya-jain/Code/PBL/data/train/attack_cleaned"
# ---------------------------

# ---------- BENIGN ----------
df = pd.read_csv(benign_file)
df["label"] = 0
df.to_csv(benign_file, index=False)

print("Labeled benign:", benign_file)


# ---------- ATTACK FILES ----------
for file in os.listdir(attack_folder):
    if file.endswith(".csv"):
        path = os.path.join(attack_folder, file)

        df = pd.read_csv(path)
        df["label"] = 1
        df.to_csv(path, index=False)

        print("Labeled attack:", file)