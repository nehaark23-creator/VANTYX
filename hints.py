import re
from collections import defaultdict
from scipy.stats import binom

CAP = 50  # each term counts max 50 clicks, so a few huge terms cannot dominate


def _tokens(q):
    return set(w for w in re.findall(r"[a-z0-9]+", str(q).lower()) if len(w) > 1)


def token_stats(df):
    """Per word: [terms, clicks, conversions, expected conversions] using each term's own campaign baseline."""
    st = defaultdict(lambda: [0, 0.0, 0.0, 0.0])
    for q, c, v, b in zip(df["query"], df["clicks"], df["conversions"], df["baseline"]):
        if c <= 0:
            continue
        cc = min(c, CAP)
        vv = v * cc / c
        ex = cc * b
        for w in _tokens(q):
            s = st[w]
            s[0] += 1
            s[1] += cc
            s[2] += vv
            s[3] += ex
    return st


def make_hint(query, tok, min_terms=30, min_clicks=200, alpha=0.001, lo=0.5, hi=1.5):
    best = None
    for w in _tokens(query):
        s = tok.get(w)
        if not s:
            continue
        terms, clicks, conv, exp = s
        if terms < min_terms or clicks < min_clicks or exp <= 0:
            continue
        ratio = conv / exp
        n = int(round(clicks))
        k = int(round(conv))
        p0 = min(max(exp / clicks, 1e-9), 1 - 1e-9)
        if ratio <= lo:
            p, lean = binom.cdf(k, n, p0), "block"
        elif ratio >= hi:
            p, lean = binom.sf(k - 1, n, p0), "promote"
        else:
            continue
        if p < alpha and (best is None or p < best[0]):
            best = (p, lean, w, ratio, terms)
    if best is None:
        return ""
    p, lean, w, ratio, terms = best
    return (f"Leans {lean}: word '{w}' converts at {ratio:.1f}x of expected "
            f"across {terms} terms (chance of luck {p:.4f}). Evidence only, human decides.")
