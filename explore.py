import pandas as pd

df = pd.read_csv("data.csv")

print("Rows, columns:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())
print("\nSummary:")
print(df.describe())

print("\nClicks distribution:")
print("terms with < 5 clicks :", (df["clicks"] < 5).mean().round(2))
print("terms with < 10 clicks:", (df["clicks"] < 10).mean().round(2))
print("terms with >= 30 clicks:", (df["clicks"] >= 30).mean().round(2))

total_clicks = df["clicks"].sum()
total_conv = df["conversions"].sum()
print("\nAccount conversion rate:", round(total_conv / total_clicks, 4))