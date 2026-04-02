import pandas as pd
import os

# ---------- PATHS ----------
benign_file = "/home/bhavya-jain/Code/PBL/data/train/multiclass_train_benign_clean.csv"
attack_folder = "/home/bhavya-jain/Code/PBL/data/train/multiclass_attack_cleaned"
# ---------------------------

def get_label(filename):
    name = filename.lower()

    if "arp" in name:
        return 4
    elif "recon" in name or "scan" in name:
        return 5
    elif "mqtt" in name:
        return 6
    elif "icmp" in name:
        return 3
    elif "udp" in name:
        return 1
    elif "tcp" in name or "syn" in name:
        return 2
    else:
        return 7  # fallback

# ---------- BENIGN ----------
df = pd.read_csv(benign_file)
df["label"] = 0
df.to_csv(benign_file, index=False)

print("Benign labeled → 0")

# ---------- ATTACK FILES ----------
for file in os.listdir(attack_folder):
    if file.endswith(".csv"):
        path = os.path.join(attack_folder, file)

        df = pd.read_csv(path)

        label = get_label(file)

        df["label"] = label
        df.to_csv(path, index=False)

        print(f"{file} → label {label}")