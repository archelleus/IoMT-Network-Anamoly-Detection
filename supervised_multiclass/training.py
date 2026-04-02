import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import time

# ---------- CONFIG ----------
DATASET = "/home/bhavya-jain/Code/PBL/data/train/multiclass_dataset.csv"
MODEL_PATH = "/home/bhavya-jain/Code/PBL/models/rf_multiclass.joblib"
MAX_PER_CLASS = 100000   # increase/decrease based on RAM
# ----------------------------

start = time.time()

print("Loading dataset...")
df = pd.read_csv(DATASET)

print("Original shape:", df.shape)

# ---------- CLEAN ----------
df = df.select_dtypes(include="number")
df = df.dropna()

# ---------- CHECK DISTRIBUTION ----------
print("\nOriginal class distribution:")
print(df["label"].value_counts())

# ---------- SMART BALANCING ----------
print("\nApplying capped balancing...")

balanced_data = []
classes = sorted(df["label"].unique())

for c in classes:
    class_df = df[df["label"] == c]
    size = len(class_df)

    if size > MAX_PER_CLASS:
        sampled = class_df.sample(n=MAX_PER_CLASS, random_state=42)
        print(f"Class {c}: reduced from {size} → {MAX_PER_CLASS}")
    else:
        sampled = class_df
        print(f"Class {c}: kept full ({size})")

    balanced_data.append(sampled)

df_balanced = pd.concat(balanced_data, ignore_index=True)

# shuffle
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

print("\nBalanced shape:", df_balanced.shape)
print("Balanced distribution:")
print(df_balanced["label"].value_counts())

# ---------- TRAIN ----------
X = df_balanced.drop(columns=["label"])
y = df_balanced["label"]

print("\nTraining multiclass model...")

model = RandomForestClassifier(
    n_estimators=250,
    n_jobs=-1,
    random_state=42
)

model.fit(X, y)

# ---------- SAVE ----------
joblib.dump(model, MODEL_PATH)

end = time.time()

print("\nModel saved:", MODEL_PATH)
print(f"Training completed in {(end - start)/60:.2f} minutes")