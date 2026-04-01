import os
import pandas as pd
import score_test_file as score

folder_path = "/home/bhavya-jain/Code/PBL/data/test/cleaned"

results = []

for name in os.listdir(folder_path):
    if name.endswith(".csv"):
        print("Processing:", name)
        res = score.scoring(name)
        results.append(res)

# --- CREATE FINAL TABLE ---
final_df = pd.DataFrame(results)

# --- SAVE ---
final_df.to_csv("attack_summary_threshold_2.csv", index=False)

print("Saved attack_summary.csv")
print(final_df)