from scipy.stats import binom
import config as C


def baseline_cvr(df):
    return df["conversions"].sum() / df["clicks"].sum()


def decide(row, base):
    n = int(row["clicks"])
    c = int(row["conversions"])
    cost = float(row["cost"])

    if n == 0:
        return "ignore", "High", "No clicks, no cost, nothing to judge"

    rate = c / n

    if n < C.MIN_CLICKS:
        return "review", "Low", (
            f"Only {n} clicks and {c} conversions, too little data to decide"
        )

    p_low = binom.cdf(c, n, base)
    p_high = binom.sf(c - 1, n, base) if c > 0 else 1.0

    if rate < base and p_low < C.ALPHA_BLOCK:
        conf = "High" if p_low < 0.001 else "Medium"
        return "block", conf, (
            f"{n} clicks, {c} conversions ({rate:.1%}) vs expected {base:.1%}; "
            f"spent {cost:.2f}; only {p_low:.1%} chance this is bad luck"
        )

    if c >= C.MIN_PROMOTE_CONV and rate >= C.MIN_LIFT * base and p_high < C.ALPHA_PROMOTE:
        conf = "High" if p_high < 0.001 else "Medium"
        return "promote", conf, (
            f"{n} clicks, {c} conversions ({rate:.1%}) vs expected {base:.1%}; "
            f"only {p_high:.1%} chance this is luck"
        )

    conf = "High" if n >= 50 else "Medium"
    return "ignore", conf, (
        f"{n} clicks, {c} conversions ({rate:.1%}); no clear difference from expected {base:.1%}"
    )

