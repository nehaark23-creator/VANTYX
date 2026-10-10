import re
import time

import pandas as pd

import config as C
from logic import baseline_cvr, decide
from hints import token_stats, make_hint

ALIASES = {
    "query": ["query", "query_text", "search_term", "search_terms", "search_query"],
    "match_type": ["match_type", "matchtype", "match"],
    "campaign": ["campaign", "campaign_name"],
    "ad_group": ["ad_group", "adgroup", "ad_group_name"],
    "impressions": ["impressions", "impr"],
    "clicks": ["clicks", "click"],
    "cost": ["cost", "spend"],
    "conversions": ["conversions", "conversion", "conv"],
    "conversion_value": ["conversion_value", "conv_value", "conversions_value", "value"],
}
REQUIRED = ["query", "clicks", "cost", "conversions"]
NUMERIC = ["impressions", "clicks", "cost", "conversions", "conversion_value"]


def _norm(c):
    return re.sub(r"[^a-z0-9]+", "_", str(c).lower()).strip("_")


def clean(df):
    df = df.rename(columns=C.RENAME)
    cols = {_norm(c): c for c in df.columns}
    mapping = {}
    for target, names in ALIASES.items():
        for n in names:
            if n in cols:
                mapping[cols[n]] = target
                break
    df = df.rename(columns=mapping)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing columns: {missing}. Found: {[str(c) for c in df.columns]}"
        )
    for c in ["match_type", "campaign", "ad_group"]:
        if c not in df.columns:
            df[c] = ""
    for c in NUMERIC:
        if c not in df.columns:
            df[c] = 0
        df[c] = pd.to_numeric(
            df[c].astype(str).str.replace(r"[^0-9.\-]", "", regex=True),
            errors="coerce",
        ).fillna(0)
    df["query"] = df["query"].astype(str)
    return df[["query", "match_type", "campaign", "ad_group", "impressions",
               "clicks", "cost", "conversions", "conversion_value"]]


def _k(s):
    return re.sub(r"\s+", " ", str(s).strip().lower())


def process(raw):
    df = clean(raw).copy()
    for col in ["match_type", "campaign", "ad_group"]:
        if col not in df.columns:
            df[col] = ""
    df["_q"] = df["query"].map(_k)
    key = ["_q", "campaign", "ad_group"]

    sums = [c for c in ["impressions", "clicks", "cost", "conversions", "conversion_value"] if c in df.columns]
    agg = {c: (c, "sum") for c in sums}
    agg["query"] = ("query", "first")
    agg["match_type"] = ("match_type", lambda s: "+".join(sorted(set(map(str, s)))))
    agg["n_rows"] = ("query", "size")
    g = df.groupby(key, sort=False, as_index=False).agg(**agg)

    acct = baseline_cvr(g)
    min_camp = getattr(C, "MIN_CAMPAIGN_CLICKS", 2000)
    camp_base = {}
    for camp, sub in g.groupby("campaign"):
        camp_base[camp] = baseline_cvr(sub) if sub["clicks"].sum() >= min_camp else acct
    g["baseline"] = g["campaign"].map(camp_base).fillna(acct)

    res = [decide(r, r["baseline"]) for _, r in g.iterrows()]
    g["decision"] = [x[0] for x in res]
    g["confidence"] = [x[1] for x in res]
    g["reason"] = [x[2] for x in res]
    pooled = g["n_rows"] > 1
    g.loc[pooled, "reason"] = g.loc[pooled, "reason"] + " (pooled over " + g.loc[pooled, "n_rows"].astype(str) + " rows)"

    g["hint"] = ""
    stats = token_stats(g)
    for i in g.index[g["decision"] == "review"]:
        g.at[i, "hint"] = make_hint(g.at[i, "query"], stats)

    return g.drop(columns=["_q"], errors="ignore")


def expand_to_rows(raw, out):
    df = clean(raw).copy()
    for col in ["campaign", "ad_group"]:
        if col not in df.columns:
            df[col] = ""
    df["_q"] = df["query"].map(_k)
    o = out.copy()
    o["_q"] = o["query"].map(_k)
    keep = ["_q", "campaign", "ad_group", "decision", "confidence", "reason", "hint", "baseline"]
    merged = df.merge(o[keep], on=["_q", "campaign", "ad_group"], how="left")
    return merged.drop(columns=["_q"])

def make_payload(out):
    df = out.copy()
    for col in ["query", "match_type", "campaign", "ad_group",
                "decision", "confidence", "reason", "hint"]:
        df[col] = df[col].fillna("").astype(str)
    df["word"] = df["hint"].str.extract(r"word '(\w+)'")[0].fillna("")
    df["lean"] = df["hint"].str.extract(r"Leans (\w+)")[0].fillna("")

    hints = {}
    for w, lean, text in zip(df["word"], df["lean"], df["hint"]):
        if w and w not in hints:
            hints[w] = {"lean": lean, "text": text}

    base = float(df["conversions"].sum() / df["clicks"].sum())
    rows = df[["query", "match_type", "campaign", "ad_group", "clicks",
               "conversions", "cost", "decision", "confidence", "reason",
               "word"]].copy()
    rows["cost"] = rows["cost"].round(2)
    rows["clicks"] = rows["clicks"].astype(int)

    return {
        "id": str(int(time.time())),
        "base": base,
        "cfg": {
            "min_clicks": C.MIN_CLICKS,
            "alpha_block": C.ALPHA_BLOCK,
            "alpha_promote": C.ALPHA_PROMOTE,
            "min_lift": C.MIN_LIFT,
            "min_promote_conv": C.MIN_PROMOTE_CONV,
        },
        "hints": hints,
        "rows": rows.values.tolist(),
    }
