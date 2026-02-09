import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# ---------- CONFIG ----------
INPUT_CSV = "train_benign_clean.csv"
SCALED_OUTPUT_CSV = "train_benign_scaled.csv"
SCALER_PATH = "scaler.joblib"
# ----------------------------

# Load cleaned training data
X_train = pd.read_csv(INPUT_CSV)

print("Loaded data shape:", X_train.shape)

# Initialize scaler
scaler = StandardScaler()

# Fit scaler ONLY on training data
X_train_scaled = scaler.fit_transform(X_train)

# Save scaler for later use on test data
joblib.dump(scaler, SCALER_PATH)
print(f"Scaler saved to {SCALER_PATH}")

# Save scaled training data
X_train_scaled_df = pd.DataFrame(
    X_train_scaled,
    columns=X_train.columns
)

X_train_scaled_df.to_csv(SCALED_OUTPUT_CSV, index=False)
print(f"Scaled training data saved to {SCALED_OUTPUT_CSV}")
