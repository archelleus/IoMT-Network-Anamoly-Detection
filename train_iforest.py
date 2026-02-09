import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# ---------- CONFIG ----------
SCALED_TRAIN_CSV = "your-file.csv" #Your training file
MODEL_PATH = "isolation_forest.joblib"
# ----------------------------

# Load scaled training data
X_train = pd.read_csv(SCALED_TRAIN_CSV)
print("Training data shape:", X_train.shape)

# Initialize Isolation Forest
model = IsolationForest(
    n_estimators=300,
    max_samples="auto",
    contamination=0.02,   # assume up to 2% anomalies
    random_state=42,
    n_jobs=-1
)

# Train model
model.fit(X_train)
print("Isolation Forest training completed.")

# Save model
joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")

# ---------- SANITY CHECK ----------
preds = model.predict(X_train)   # -1 = anomaly, 1 = normal
anomalies = (preds == -1).sum()

print("Anomalies flagged in training data:", anomalies)
print("Fraction anomalous:", anomalies / len(preds))
