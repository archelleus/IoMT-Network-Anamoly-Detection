import pandas as pd

df = pd.read_csv("rf_multiclass_summary.csv")

# ---------- MAP CLASS NAMES ----------
label_names = {
    0: "benign",
    1: "udp",
    2: "tcp",
    3: "icmp",
    4: "arp",
    5: "recon",
    6: "mqtt"
}

df["predicted_type"] = df["dominant_class"].map(label_names)

# ---------- CONFIDENCE LEVEL ----------
df["confidence"] = df["dominant_fraction"].apply(
    lambda x: "High" if x > 0.8 else "Medium" if x > 0.5 else "Low"
)

# ---------- SORT ----------
df = df.sort_values(by="dominant_fraction", ascending=False)

# ---------- SAVE ----------
df.to_csv("rf_multiclass_evaluation.csv", index=False)

print(df)