import pandas as pd

def compute_summary(df):
    # simple aggregates: pct change vs stored previous day if available
    grouped = df.copy()
    grouped = grouped.sort_values(["target_currency"])
    # top 5 by rate (absolute)
    top5 = grouped.nlargest(5, "rate")
    lines = []
    lines.append("Top 5 por taxa:")
    for _, r in top5.iterrows():
        lines.append(f"{r['target_currency']}: {r['rate']}")
    return "\n".join(lines)
