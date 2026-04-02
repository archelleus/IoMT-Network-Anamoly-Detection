import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import numpy as np
# ---------- CONFIG ----------
SCALED_TRAIN_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/train/train_benign_scaled.csv")
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../models/isolation_forest.joblib")
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

# ---------- THRESHOLD CALCULATION ----------
train_scores = model.decision_function(X_train)

threshold = np.percentile(train_scores, 2)   # start with 5%
print("Learned threshold:", threshold)

joblib.dump(threshold, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../models/threshold.joblib"))
print("Threshold saved to threshold.joblib")