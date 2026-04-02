import pandas as pd
import numpy as np
import joblib

import os
model_path = os.path.join(os.path.dirname(__file__), "../../models/rf_model.joblib")
model = joblib.load(model_path)

def scoring(file):
    import os
    test_dir = os.path.join(os.path.dirname(__file__), "../../data/test/cleaned")
    df = pd.read_csv(os.path.join(test_dir, file))

    # --- CLEAN ---
    df = df.select_dtypes(include="number")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.dropna()

    # --- REMOVE LABEL IF PRESENT ---
    if "label" in df.columns:
        df = df.drop(columns=["label"])

    # --- PREDICT ---
    preds = model.predict(df)

    total = len(preds)
    attacks = (preds == 1).sum()
    normal = (preds == 0).sum()

    fraction = attacks / total if total > 0 else 0

    return {
        "file": file,
        "total_samples": total,
        "predicted_attacks": int(attacks),
        "predicted_normal": int(normal),
        "attack_fraction": float(fraction)
    }