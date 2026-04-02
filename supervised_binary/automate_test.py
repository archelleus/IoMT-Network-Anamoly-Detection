import os
import pandas as pd
import time
import score_test_file as score

folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test/cleaned")

results = []

start = time.time()

files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

print(f"Found {len(files)} files\n")

for i, name in enumerate(files, 1):
    t0 = time.time()

    print(f"[{i}/{len(files)}] Processing: {name}")

    res = score.scoring(name)
    results.append(res)

    t1 = time.time()
    print(f"Done in {t1 - t0:.2f}s\n")

# --- CREATE FINAL TABLE ---
final_df = pd.DataFrame(results)

# --- SORT (optional but useful) ---
final_df = final_df.sort_values(by="attack_fraction", ascending=False)

# --- SAVE ---
output_file = "rf_attack_summary.csv"
final_df.to_csv(output_file, index=False)

end = time.time()

print(f"\nSaved: {output_file}")
print(f"Total time: {end - start:.2f}s")

print("\nPreview:")
print(final_df.head())