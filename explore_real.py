import sys
import pandas as pd

path = sys.argv[1] if len(sys.argv) > 1 else "real.csv"
df = pd.read_csv(path, encoding_errors="replace")

print("Rows, columns:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head().to_string())
print("\nDtypes:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())

for c in df.columns:
    if df[c].dtype == object and any(k in c.lower() for k in ["cost", "spend", "value", "click", "conv", "impr"]):
        print(f"\nWARNING: '{c}' is text, not numeric. Sample:", df[c].head(3).tolist())

num = df.select_dtypes("number")
print("\nSummary:")
print(num.describe().T.to_string())

cols = {c.lower(): c for c in df.columns}
def pick(*names):
    for n in names:
        for k, v in cols.items():
            if n in k:
                return v

ck = pick("click")
cv = pick("conversions", "conv")
if ck and cv and pd.api.types.is_numeric_dtype(df[ck]):
    print("\nTerms with < 5 clicks :", round((df[ck] < 5).mean(), 2))
    print("Terms with < 10 clicks:", round((df[ck] < 10).mean(), 2))
    print("Terms with >= 30 clicks:", round((df[ck] >= 30).mean(), 2))
    if pd.api.types.is_numeric_dtype(df[cv]):
        print("Account conversion rate:", round(df[cv].sum() / df[ck].sum(), 4))
        print("Terms with conversions > 0:", round((df[cv] > 0).mean(), 3))

q = pick("query", "search term", "search_term")
if q:
    print("\nDuplicate query rows:", df[q].duplicated().sum())
    print("Unique queries:", df[q].nunique())
    print("\nSample queries:")
    print(df[q].sample(15, random_state=1).tolist())
