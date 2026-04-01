import os
import pandas as pd
import numpy as np

TRAIN_DIR = "/home/bhavya-jain/Code/PBL/data/train/attack_cleaned"   # path to train folder

def clean_df(df):
    # keep only numeric columns (behavioral features)
    df = df.select_dtypes(include="number")

    # replace inf with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # drop rows with NaN
    df = df.dropna()

    return df

all_dfs = []

for file in os.listdir(TRAIN_DIR):
    if file.endswith(".csv"):
        path = os.path.join(TRAIN_DIR, file)
        print(f"Processing {file}...")

        df = pd.read_csv(path)
        df = clean_df(df)

        all_dfs.append(df)

# merge all train files
train_merged = pd.concat(all_dfs, ignore_index=True)

print("\nFinal merged TRAIN shape:", train_merged.shape)

# save merged train data
train_merged.to_csv("train_merged.csv", index=False)
print("Saved train_merged.csv")
