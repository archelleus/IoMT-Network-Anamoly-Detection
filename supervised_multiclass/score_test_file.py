import pandas as pd
import numpy as np
import joblib

# load multiclass model
import os
model_path = os.path.join(os.path.dirname(__file__), "../../models/rf_multiclass.joblib")
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

    # count per class
    unique, counts = np.unique(preds, return_counts=True)
    class_counts = dict(zip(unique, counts))

    # dominant class
    dominant_class = max(class_counts, key=class_counts.get)
    dominant_fraction = class_counts[dominant_class] / total if total > 0 else 0

    # result dict
    result = {
        "file": file,
        "total_samples": total,
        "dominant_class": int(dominant_class),
        "dominant_fraction": float(dominant_fraction),
    }

    # include all class counts (0–6)
    for c in range(7):
        result[f"class_{c}"] = int(class_counts.get(c, 0))

    return result