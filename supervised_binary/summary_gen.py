import pandas as pd

df = pd.read_csv("rf_attack_summary.csv")

# classify type (same logic)
df["type"] = df["file"].apply(
    lambda x: "benign" if "benign" in x.lower() else "attack"
)

# detection quality based on attack_fraction
df["detection_quality"] = df["attack_fraction"].apply(
    lambda x: "High" if x > 0.7 else "Medium" if x > 0.2 else "Low"
)

# sort by strength
df = df.sort_values(by="attack_fraction", ascending=False)

# save
df.to_csv("rf_final_evaluation.csv", index=False)

print(df)