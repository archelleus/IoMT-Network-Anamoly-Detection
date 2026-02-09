import pandas as pd
import numpy as np
import joblib

def scoring(file):
    scaler = joblib.load("scaler.joblib")
    model = joblib.load("isolation_forest.joblib")

# Load test data
    df = pd.read_csv("cleaned_test/"+file)

# --- CLEAN (same as training) ---
    df = df.select_dtypes(include="number")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.dropna()

# --- SCALE (THIS WAS MISSING) ---
    X_test_scaled = pd.DataFrame(
        scaler.transform(df),
        columns=df.columns
    )

# --- SCORE ---
    scores = model.decision_function(X_test_scaled)
    preds = model.predict(X_test_scaled)

    print("Total samples:", len(preds))
    print("Anomalies detected:", (preds == -1).sum())
    print("Fraction anomalous:", (preds == -1).sum() / len(preds))

    print("Score stats:", scores.min(), scores.mean(), scores.max())
