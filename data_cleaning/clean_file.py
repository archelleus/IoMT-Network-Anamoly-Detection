import pandas as pd
import numpy as np

df = pd.read_csv("train/benign_train.csv")

df = df.select_dtypes(include="number")
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df = df.dropna()

df.to_csv("/home/bhavya-jain/Code/PBL/data/train/supervised_train_benign_clean.csv", index=False)
