import pandas as pd

df = pd.read_csv("real.csv")
q = df["search_term"].str.lower().str.strip()

print("== Data quality ==")
print("zero-click rows:", (df.clicks == 0).sum(), round((df.clicks == 0).mean(), 3))
print("conversions > clicks:", (df.conversions > df.clicks).sum())
print("clicks > impressions:", (df.clicks > df.impressions).sum())
print("cost>0 but clicks=0:", ((df.cost > 0) & (df.clicks == 0)).sum())
print("clicks>0 but cost=0:", ((df.clicks > 0) & (df.cost == 0)).sum())
print("conv_value>0 but conv=0:", ((df.conversion_value > 0) & (df.conversions == 0)).sum())
print("conv>0 but value=0:", ((df.conversions > 0) & (df.conversion_value == 0)).sum())

print("\n== Duplicates ==")
k = ["search_term", "campaign", "ad_group"]
print("same query+campaign+ad_group:", df.duplicated(k).sum())
print("same query+campaign+ad_group+match_type:", df.duplicated(k + ["match_type"]).sum())
print("fully identical rows (ignoring row_id):", df.drop(columns="row_id").duplicated().sum())
print("queries in more than 1 campaign:", (df.groupby("search_term").campaign.nunique() > 1).sum())
print("unique raw / after lower+strip:", df.search_term.nunique(), q.nunique())

print("\n== Pooling per query ==")
pool = df.groupby(q).clicks.sum()
print("row-level < 10 clicks:", round((df.clicks < 10).mean(), 3))
print("query-level < 10 clicks:", round((pool < 10).mean(), 3))

def split(col):
    g = df.groupby(col).agg(rows=("clicks", "size"), clicks=("clicks", "sum"),
                            conv=("conversions", "sum"), cost=("cost", "sum"),
                            value=("conversion_value", "sum"))
    g["cvr"] = g.conv / g.clicks
    g["cpc"] = g.cost / g.clicks
    g["roas"] = g.value / g.cost
    return g.sort_values("clicks", ascending=False).round(3)

print("\n== By campaign ==")
print(split("campaign").to_string())
print("\n== By match type ==")
print(split("match_type").to_string())

print("\n== Top 10 spend with zero conversions ==")
z = df[df.conversions == 0].sort_values("cost", ascending=False).head(10)
print(z[["search_term", "campaign", "clicks", "cost"]].to_string(index=False))
