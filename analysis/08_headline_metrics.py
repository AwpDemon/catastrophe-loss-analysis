"""
08_headline_metrics.py: compute every number quoted in README.md.

Writes reports/headline_metrics.json. tests/test_readme_numbers.py fails if
the README disagrees with it. Data is synthetic (data/generate_sales_data.py).
"""

import json
import os

import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data", "kat_insurance_sales.csv")
OUT = os.path.join(BASE, "..", "reports", "headline_metrics.json")


def lr(g: pd.DataFrame) -> float:
    return g["claim_amount"].sum() / g["net_premium"].sum()


def main() -> None:
    df = pd.read_csv(DATA, parse_dates=["transaction_date"])
    df["year"] = df["transaction_date"].dt.year
    df["quarter"] = df["transaction_date"].dt.quarter
    m: dict = {}

    m["rows"] = int(len(df))
    m["product_lines"] = int(df["product_line"].nunique())
    m["regions"] = int(df["region"].nunique())
    m["states"] = int(df["state"].nunique())
    m["years"] = sorted(int(y) for y in df["year"].unique())
    m["net_premium_musd"] = round(df["net_premium"].sum() / 1e6, 2)
    m["loss_ratio_pct"] = round(lr(df) * 100, 2)
    exp = (df["commission"].sum() + df["admin_cost"].sum()) / df["net_premium"].sum()
    m["expense_ratio_pct"] = round(exp * 100, 2)
    m["combined_ratio_pct"] = round((lr(df) + exp) * 100, 2)

    # Q3 spike: pooled loss ratio and monthly-level test
    q3, rest = df[df["quarter"] == 3], df[df["quarter"] != 3]
    m["q3_loss_ratio_pct"] = round(lr(q3) * 100, 1)
    m["other_quarters_loss_ratio_pct"] = round(lr(rest) * 100, 1)
    m["q3_spike_points"] = round((lr(q3) - lr(rest)) * 100, 1)

    # Attribution of Q3 excess claims to the FL + Gulf Coast Home segment:
    # excess = Q3 claims minus what the segment's own rest-of-year loss ratio implies.
    excess_total = q3["claim_amount"].sum() - lr(rest) * q3["net_premium"].sum()
    seg = (df["product_line"] == "Home") & df["region"].isin(["Florida", "Gulf Coast"])
    q3s, rests = q3[seg.loc[q3.index]], rest[seg.loc[rest.index]]
    excess_seg = q3s["claim_amount"].sum() - lr(rests) * q3s["net_premium"].sum()
    m["fl_gulf_home_share_of_q3_excess_pct"] = round(excess_seg / excess_total * 100, 1)
    m["fl_gulf_home_share_of_premium_pct"] = round(df.loc[seg, "net_premium"].sum() / df["net_premium"].sum() * 100, 1)

    # YoY premium growth and mix shift by line
    yy = df.groupby(["year", "product_line"])["net_premium"].sum().unstack(0)
    m["yoy_growth_pct"] = {k: round(float(v), 1) for k, v in ((yy[2023] / yy[2022] - 1) * 100).items()}
    mix = yy / yy.sum() * 100
    m["mix_shift_pp"] = {k: round(float(v), 1) for k, v in (mix[2023] - mix[2022]).items()}
    m["uw_margin_by_line_pct"] = {
        k: round(float(g["underwriting_result"].sum() / g["net_premium"].sum() * 100), 1)
        for k, g in df.groupby("product_line")}

    # Churn by tenure
    churned = df["policy_status"].isin(["Cancelled", "Lapsed"])
    bucket = pd.cut(df["policy_tenure_months"], [-1, 12, 36, 1e6], labels=["0-12mo", "13-36mo", "37+mo"])
    rates = churned.groupby(bucket, observed=True).mean() * 100
    m["churn_by_tenure_pct"] = {str(k): round(float(v), 2) for k, v in rates.items()}
    chi2, p, dof, _ = stats.chi2_contingency(pd.crosstab(bucket, churned))
    m["churn_chi2"] = {"chi2": round(float(chi2), 1), "df": int(dof), "p": float(f"{p:.3g}")}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2)
    print(json.dumps(m, indent=2))


if __name__ == "__main__":
    main()
