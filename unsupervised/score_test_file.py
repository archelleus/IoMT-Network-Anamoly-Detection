import pandas as pd
import numpy as np
import joblib

scaler_path = os.path.join(os.path.dirname(__file__), "../../models/scaler.joblib")
scaler = joblib.load(scaler_path)
import os
model_path = os.path.join(os.path.dirname(__file__), "../../models/isolation_forest.joblib")
model = joblib.load(model_path)

def scoring(file):
    import os
test_dir = os.path.join(os.path.dirname(__file__), "../../data/test/cleaned")
    df = pd.read_csv(os.path.join(test_dir, file))

    # --- CLEAN ---
    df = df.select_dtypes(include="number")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.dropna()

    # --- SCALE ---
    X_test_scaled = pd.DataFrame(
        scaler.transform(df),
        columns=df.columns
    )

    # --- SCORE ---
    threshold_path = os.path.join(os.path.dirname(__file__), "../../models/threshold.joblib")
threshold = joblib.load(threshold_path)
    scores = model.decision_function(X_test_scaled)
    preds = np.where(scores < threshold, -1, 1)

    total = len(preds)
    anomalies = (preds == -1).sum()
    fraction = anomalies / total if total > 0 else 0

    return {
        "file": file,
        "total_samples": total,
        "anomalies": anomalies,
        "fraction_anomalous": fraction,
        "min_score": float(scores.min()),
        "mean_score": float(scores.mean()),
        "max_score": float(scores.max())
    }