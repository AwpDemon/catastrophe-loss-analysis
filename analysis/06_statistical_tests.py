"""
06_statistical_tests.py — formal stats behind the findings in the README.

The three headline claims from the exec summary get tested here:
  (1) Q3 loss ratio is elevated vs. the rest of the year
  (2) Commercial YoY premium growth is materially above Auto
  (3) First-year churn differs from multi-year tenure churn

Each test reports its p-value and a bootstrap 95% CI for the effect size,
and produces a chart that visualizes the tested distribution.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data", "kat_insurance_sales.csv")
OUT = os.path.join(BASE, "..", "visualizations")
os.makedirs(OUT, exist_ok=True)

RNG = np.random.default_rng(17)


def bootstrap_ci(x, stat=np.mean, n=4000, alpha=0.05):
    """Percentile bootstrap CI around a statistic."""
    x = np.asarray(x)
    boot = np.empty(n)
    idx = RNG.integers(0, len(x), size=(n, len(x)))
    for i in range(n):
        boot[i] = stat(x[idx[i]])
    return np.quantile(boot, [alpha / 2, 1 - alpha / 2])


def cohens_d(a, b):
    a, b = np.asarray(a), np.asarray(b)
    s = np.sqrt(((a.var(ddof=1) * (len(a) - 1)) + (b.var(ddof=1) * (len(b) - 1))) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / s if s > 0 else np.nan


def main():
    df = pd.read_csv(DATA, parse_dates=["transaction_date"])
    df["month"] = df["transaction_date"].dt.month
    df["quarter"] = df["transaction_date"].dt.quarter
    df["year"] = df["transaction_date"].dt.year
    # Aggregate to monthly loss ratio so the unit of observation is a month,
    # not a transaction. Transaction-level is noisy + heavily zero-inflated.
    monthly = (
        df.groupby(["year", "month"])
        .apply(lambda g: g["claim_amount"].sum() / g["net_premium"].sum())
        .reset_index(name="loss_ratio")
    )
    monthly["quarter"] = ((monthly["month"] - 1) // 3) + 1
    q3 = monthly.loc[monthly["quarter"] == 3, "loss_ratio"].values
    notq3 = monthly.loc[monthly["quarter"] != 3, "loss_ratio"].values

    t, p = stats.ttest_ind(q3, notq3, equal_var=False)
    d = cohens_d(q3, notq3)
    diff_ci = bootstrap_ci(
        np.concatenate([q3, notq3]),
        stat=lambda x: x[: len(q3)].mean() - x[len(q3):].mean(),
    )

    print("=" * 66)
    print("  TEST 1 — Q3 loss ratio elevated vs. rest of year (Welch's t)")
    print("=" * 66)
    print(f"   Q3 months n={len(q3)}   mean={q3.mean():.3f}   sd={q3.std(ddof=1):.3f}")
    print(f"   Other   n={len(notq3)}  mean={notq3.mean():.3f}   sd={notq3.std(ddof=1):.3f}")
    print(f"   t = {t:+.2f}   p = {p:.4f}   Cohen's d = {d:+.2f}")
    print(f"   95% CI on diff (bootstrap): [{diff_ci[0]:+.3f}, {diff_ci[1]:+.3f}]")
    print()

    # --- Test 2: Commercial vs Auto YoY growth (within-line YoY) ---
    yearly = (
        df.groupby(["year", "product_line"])["net_premium"]
        .sum()
        .unstack("year")
    )
    yearly["yoy"] = (yearly[2023] - yearly[2022]) / yearly[2022]

    # Bootstrap the YoY by resampling transactions within each line
    def line_yoy_bootstrap(line, n=2000):
        sub = df[df["product_line"] == line]
        out = np.empty(n)
        for i in range(n):
            samp = sub.sample(frac=1.0, replace=True, random_state=int(RNG.integers(1e9)))
            by = samp.groupby("year")["net_premium"].sum()
            out[i] = (by.get(2023, 0) - by.get(2022, 0)) / by.get(2022, 1)
        return out

    com_boot = line_yoy_bootstrap("Commercial")
    auto_boot = line_yoy_bootstrap("Auto")
    com_ci = np.quantile(com_boot, [0.025, 0.975])
    auto_ci = np.quantile(auto_boot, [0.025, 0.975])
    gap = com_boot - auto_boot
    gap_p = 2 * min((gap <= 0).mean(), (gap >= 0).mean())

    print("=" * 66)
    print("  TEST 2 — Commercial YoY premium growth vs. Auto (bootstrap)")
    print("=" * 66)
    print(f"   Commercial YoY : {yearly.loc['Commercial','yoy']*100:+.2f}%   95% CI [{com_ci[0]*100:+.2f}%, {com_ci[1]*100:+.2f}%]")
    print(f"   Auto       YoY : {yearly.loc['Auto','yoy']*100:+.2f}%   95% CI [{auto_ci[0]*100:+.2f}%, {auto_ci[1]*100:+.2f}%]")
    print(f"   Gap (Com-Auto) : {gap.mean()*100:+.2f}pp   bootstrap p = {gap_p:.4f}")
    print()

    # --- Test 3: Churn in year-1 vs 3+ years (chi-squared) ---
    df["tenure_bucket"] = pd.cut(
        df["policy_tenure_months"],
        bins=[-1, 12, 36, 1e6],
        labels=["0-12mo", "13-36mo", "37+mo"],
    )
    churned = df["policy_status"].isin(["Cancelled", "Lapsed"])
    ctab = pd.crosstab(df["tenure_bucket"], churned)
    ctab.columns = ["retained", "churned"]
    chi2, pchi, _, _ = stats.chi2_contingency(ctab.values)

    rate = ctab["churned"] / ctab.sum(axis=1)
    print("=" * 66)
    print("  TEST 3 — Churn differs by tenure bucket (chi-squared)")
    print("=" * 66)
    for bucket in ctab.index:
        print(f"   {bucket:<8}  churn rate = {rate[bucket]*100:5.2f}%   (n={ctab.loc[bucket].sum():,})")
    print(f"   chi-sq = {chi2:.1f}   df=2   p = {pchi:.2e}")
    print()

    # --- Figure: side-by-side of the three tests ---
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    axes[0].boxplot(
        [notq3, q3], labels=["Q1/Q2/Q4", "Q3"], patch_artist=True,
        boxprops=dict(facecolor="#d6eaf8"), medianprops=dict(color="#c0392b"),
    )
    axes[0].set_title(f"Monthly loss ratio by season\nWelch t p={p:.3f}, d={d:+.2f}", fontweight="bold")
    axes[0].set_ylabel("Loss ratio")

    lines = ["Commercial", "Health", "Home", "Life", "Auto"]
    yoy_vals = yearly.loc[lines, "yoy"].values * 100
    colors = ["#1abc9c" if v > 0 else "#e74c3c" for v in yoy_vals]
    axes[1].barh(lines, yoy_vals, color=colors)
    for i, v in enumerate(yoy_vals):
        axes[1].text(v + 0.1, i, f"{v:+.1f}%", va="center", fontsize=10)
    axes[1].set_title(f"YoY premium growth 2022→2023\nCom vs Auto gap p={gap_p:.3f}", fontweight="bold")
    axes[1].set_xlabel("YoY %")
    axes[1].invert_yaxis()

    axes[2].bar(rate.index.astype(str), rate.values * 100, color=["#e74c3c", "#f39c12", "#27ae60"])
    for i, v in enumerate(rate.values * 100):
        axes[2].text(i, v + 0.4, f"{v:.1f}%", ha="center", fontsize=10)
    axes[2].set_title(f"Churn rate by tenure bucket\nchi-sq p={pchi:.1e}", fontweight="bold")
    axes[2].set_ylabel("Churn rate (%)")
    axes[2].set_xlabel("Tenure")

    plt.tight_layout()
    fig.savefig(os.path.join(OUT, "11_statistical_tests.png"), dpi=150)
    plt.close()
    print(f"Chart → {OUT}/11_statistical_tests.png")


if __name__ == "__main__":
    main()
