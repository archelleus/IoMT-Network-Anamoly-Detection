import pandas as pd

df = pd.read_csv("output_csv/attack_summary_threshold_5.csv")

# classify type
df["type"] = df["file"].apply(
    lambda x: "benign" if "benign" in x.lower() else "attack"
)

# detection quality
df["detection_quality"] = df["fraction_anomalous"].apply(
    lambda x: "High" if x > 0.7 else "Medium" if x > 0.2 else "Low"
)

# sort
df = df.sort_values(by="fraction_anomalous", ascending=False)

df.to_csv("final_evaluation_threshold_5.csv", index=False)
print(df)