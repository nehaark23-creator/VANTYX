import pandas as pd

d = pd.read_csv("output.csv")
h = d[d["hint"].notna() & (d["hint"] != "")]
w = h["hint"].str.extract(r"Leans (\w+): word '(\w+)'")
w.columns = ["lean", "word"]
print(w.value_counts())