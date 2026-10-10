from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Search Term Triage", layout="centered")

DATA = "output.csv"
CORR = "corrections.csv"


@st.cache_data
def load():
    d = pd.read_csv(DATA)
    d["hint"] = d["hint"].fillna("")
    ex = d["hint"].str.extract(r"Leans (\w+): word '(\w+)'")
    d["lean"] = ex[0].fillna("")
    d["word"] = ex[1].fillna("")
    d["key"] = (
        d["query"].astype(str) + " | " + d["campaign"].astype(str)
        + " | " + d["ad_group"].astype(str)
    )
    return d


if not Path(DATA).exists():
    st.error("output.csv not found. Run: python run.py")
    st.stop()

df = load()

if "corr" not in st.session_state:
    if Path(CORR).exists():
        c = pd.read_csv(CORR)
        st.session_state.corr = dict(zip(c["key"], c["decision"]))
    else:
        st.session_state.corr = {}


def apply_decision(keys, decision):
    for k in keys:
        st.session_state.corr[k] = decision
    pd.DataFrame(
        {"key": list(st.session_state.corr.keys()),
         "decision": list(st.session_state.corr.values())}
    ).to_csv(CORR, index=False)


def reset_all():
    st.session_state.corr = {}
    if Path(CORR).exists():
        Path(CORR).unlink()


corr = st.session_state.corr
df = df.copy()
df["reviewed"] = df["key"].isin(corr.keys())
df["final"] = df["key"].map(corr).fillna(df["decision"])
df["source"] = df["reviewed"].map({True: "reviewer", False: "model"})

# ---------- Header ----------
st.title("Search Term Triage")
st.caption("Every term gets a decision. Terms with too little data are left for a human.")

# ---------- 4 numbers ----------
n = df["final"].value_counts()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Promote", f"{n.get('promote', 0):,}")
c2.metric("Block", f"{n.get('block', 0):,}")
c3.metric("Ignore", f"{n.get('ignore', 0):,}")
c4.metric("Needs review", f"{n.get('review', 0):,}")

st.divider()

# ---------- Review ----------
pending = df[(df["decision"] == "review") & (~df["reviewed"])]
with_hint = pending[pending["word"] != ""]
no_hint = pending[pending["word"] == ""]

st.subheader("Review")

if with_hint.empty:
    st.success("All groups with evidence are reviewed.")
else:
    g = (
        with_hint.groupby(["word", "lean"])
        .agg(terms=("query", "count"))
        .reset_index()
        .sort_values("terms", ascending=False)
    )
    labels = {
        f"{r.word}  ·  {r.terms} terms  ·  leans {r.lean}": r.word
        for r in g.itertuples()
    }
    pick = st.selectbox("Word group", list(labels.keys()))
    word = labels[pick]
    sub = with_hint[with_hint["word"] == word]
    lean = sub["lean"].iloc[0]
    keys = sub["key"].tolist()

    st.info(sub["hint"].iloc[0])

    b1, b2, b3 = st.columns(3)
    for col, name in zip((b1, b2, b3), ("promote", "block", "ignore")):
        col.button(
            f"{name.capitalize()} all {len(sub)}",
            on_click=apply_decision,
            args=(keys, name),
            key=f"btn_{name}",
            type="primary" if name == lean else "secondary",
            use_container_width=True,
        )

    st.caption("Highest-cost terms in this group")
    st.dataframe(
        sub.sort_values("cost", ascending=False)
        .head(8)[["query", "clicks", "conversions", "cost"]],
        hide_index=True,
        use_container_width=True,
    )

if len(no_hint):
    st.caption(
        f"{len(no_hint):,} more terms have too little data and no word-level "
        "evidence. They stay in review."
    )

# ---------- Sidebar: export ----------
with st.sidebar:
    st.header("Export")
    cols = ["query", "match_type", "campaign", "ad_group", "final",
            "confidence", "reason", "source"]
    st.download_button(
        "All decisions",
        df[cols].to_csv(index=False).encode("utf-8"),
        "triage_decisions.csv",
        use_container_width=True,
    )
    st.download_button(
        "Negatives (block)",
        df[df["final"] == "block"][["query", "match_type", "campaign", "ad_group"]]
        .to_csv(index=False).encode("utf-8"),
        "negatives.csv",
        use_container_width=True,
    )
    st.download_button(
        "New keywords (promote)",
        df[df["final"] == "promote"][["query", "match_type", "campaign", "ad_group"]]
        .to_csv(index=False).encode("utf-8"),
        "keywords.csv",
        use_container_width=True,
    )
    st.divider()
    st.button("Reset reviewer decisions", on_click=reset_all,
              use_container_width=True)