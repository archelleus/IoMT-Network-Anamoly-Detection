import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import time

# ---------- CONFIG ----------
DATASET = "/home/bhavya-jain/Code/PBL/data/train/binary_dataset.csv"
MODEL_PATH = "/home/bhavya-jain/Code/PBL/models/rf_model.joblib"
# ----------------------------

start = time.time()

print("Loading dataset...")
df = pd.read_csv(DATASET)

print("Shape:", df.shape)

# ---------- CLEAN ----------
df = df.select_dtypes(include="number")
df = df.dropna()

# ---------- BALANCE ----------
benign = df[df["label"] == 0]
attack = df[df["label"] == 1]

n = len(benign)
attack_sample = attack.sample(n=n, random_state=42)

df_balanced = pd.concat([benign, attack_sample], ignore_index=True)

# shuffle
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

print("Balanced shape:", df_balanced.shape)

# ---------- TRAIN ----------
X = df_balanced.drop(columns=["label"])
y = df_balanced["label"]

print("Training model...")

model = RandomForestClassifier(
    n_estimators=250,
    n_jobs=-1,
    random_state=42
)

model.fit(X, y)

# ---------- SAVE ----------
joblib.dump(model, MODEL_PATH)

end = time.time()

print("Model saved:", MODEL_PATH)
print(f"Training completed in {(end - start)/60:.2f} minutes")