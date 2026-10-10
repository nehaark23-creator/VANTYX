import sys

import pandas as pd

from pipeline import process, expand_to_rows

path = sys.argv[1] if len(sys.argv) > 1 else "real.csv"
raw = pd.read_csv(path, encoding_errors="replace")
out = process(raw)

out.to_csv("output.csv", index=False)
expand_to_rows(raw, out).to_csv("output_by_row.csv", index=False)
out[out["decision"] == "review"].to_csv("review_queue.csv", index=False)

print("Input rows:", len(raw), "-> unique terms:", len(out))
print("\nDecisions:")
print(out["decision"].value_counts())
print("\nConfidence:")
print(out["confidence"].value_counts())
print("\nReview terms with a hint:",
      (out["hint"] != "").sum(), "of", (out["decision"] == "review").sum())

print("\nTop spend with zero conversions, and what we decided:")
z = out[out["conversions"] == 0].sort_values("cost", ascending=False).head(10)
print(z[["query", "clicks", "cost", "decision"]].to_string(index=False))

print("\nSample:")
for d in ["promote", "block", "ignore", "review"]:
    for _, r in out[out["decision"] == d].head(3).iterrows():
        print(f"[{d}] {r['query']}: {r['reason']}")
