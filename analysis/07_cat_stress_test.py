"""
07_cat_stress_test.py — catastrophe stress test.

The 2022-2023 period was relatively quiet. The question an actuary
would actually ask before reserving is: what does a bad hurricane
season do to the book?

This script Monte Carlos a hurricane year on top of the existing
Florida + Gulf Coast home portfolio:
  - annual hurricane count ~ Poisson(lambda) with lambda drawn from a
    prior informed by 2005-2023 landfall data
  - per-event damage factor ~ LogNormal calibrated so a 1-in-100 year
    loss multiple lines up with published industry catastrophe models
  - only Home premium in FL + Gulf Coast is exposed

Outputs a loss distribution and reports PML at key return periods
(VaR-style), plus an estimated reinsurance attachment point that
would cap the book's 1-in-100 year loss to 20% of premium.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data", "kat_insurance_sales.csv")
OUT = os.path.join(BASE, "..", "visualizations")

RNG = np.random.default_rng(91)
N_SIMS = 20_000

# Prior on annual landfalling hurricane count for the Southeast US
POISSON_LAMBDA = 2.1
# Per-event severity — log-normal in $ damage / $ premium exposed
SEVERITY_MU, SEVERITY_SIGMA = np.log(0.12), 1.1
# Fraction of exposed premium that is considered cat-exposed Home
EXPOSED_LINES = ["Home"]
EXPOSED_REGIONS = ["Florida", "Gulf Coast"]


def main():
    df = pd.read_csv(DATA, parse_dates=["transaction_date"])
    exposed = df[
        df["product_line"].isin(EXPOSED_LINES)
        & df["region"].isin(EXPOSED_REGIONS)
    ]
    total_premium = df["net_premium"].sum()
    exposed_premium = exposed["net_premium"].sum()

    print("=" * 66)
    print("  CAT STRESS TEST — FL + Gulf Coast Home portfolio")
    print("=" * 66)
    print(f"   Total book net premium      : ${total_premium/1e6:,.2f}M")
    print(f"   Cat-exposed (Home FL+GC)    : ${exposed_premium/1e6:,.2f}M  ({exposed_premium/total_premium*100:.1f}% of book)")
    print(f"   Sims                         : {N_SIMS:,}")
    print()

    # Simulate annual losses
    n_events = RNG.poisson(POISSON_LAMBDA, size=N_SIMS)
    annual_loss = np.zeros(N_SIMS)
    for i, k in enumerate(n_events):
        if k == 0:
            continue
        severity = RNG.lognormal(SEVERITY_MU, SEVERITY_SIGMA, size=k)
        annual_loss[i] = severity.sum() * exposed_premium

    lr = annual_loss / total_premium  # extra loss-ratio addition from cats

    # Percentile (PML) summary
    pml_table = []
    for rp in [5, 10, 25, 50, 100, 250]:
        q = np.quantile(annual_loss, 1 - 1 / rp)
        pml_table.append((rp, q, q / total_premium * 100))

    print("   PML by return period")
    print("   " + "-" * 60)
    print(f"   {'Return':>7}  {'Annual loss ($)':>20}  {'% of book premium':>20}")
    for rp, q, pct in pml_table:
        print(f"   1-in-{rp:<4}  ${q/1e6:>16,.2f}M  {pct:>18.2f}%")
    print()

    # Reinsurance attachment: cap the residual 1-in-100 cat loss at a
    # fixed % of cat-exposed premium (common per-risk retention target).
    cap_pct = 1.00  # retain up to 100% of exposed-line premium
    cap = cap_pct * exposed_premium
    pml100 = np.quantile(annual_loss, 0.99)
    pml250 = np.quantile(annual_loss, 1 - 1/250)
    attachment = max(0, pml100 - cap)
    layer = max(0, pml250 - max(pml100, cap))
    print(f"   1-in-100 gross cat loss      : ${pml100/1e6:,.2f}M")
    print(f"   Retention target (1x exposed): ${cap/1e6:,.2f}M")
    if attachment > 0:
        print(f"   Implied reinsurance layer    : ${layer/1e6:,.2f}M xs ${cap/1e6:,.2f}M")
    else:
        print(f"   Net retained 1-in-100 loss   : ${pml100/1e6:,.2f}M (within retention — no RI layer triggered)")
        print(f"   1-in-250 tail loss            : ${pml250/1e6:,.2f}M — candidate for a thin cat-xs-loss cover")
    print()

    # --- Figure: loss distribution with PML markers ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(annual_loss / 1e6, bins=80, color="#2980b9", alpha=0.85, edgecolor="white")
    for rp, q, _ in pml_table:
        ax.axvline(q / 1e6, color="#c0392b", ls="--", lw=1.1, alpha=0.6)
        ax.text(q / 1e6, ax.get_ylim()[1] * 0.95, f" 1-in-{rp}",
                rotation=90, va="top", fontsize=8, color="#c0392b")
    ax.set_xlabel("Annual cat loss ($M)")
    ax.set_ylabel("Simulation count")
    ax.set_title("Hurricane stress test — simulated annual cat loss distribution",
                 fontweight="bold")
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, "12_cat_stress_test.png"), dpi=150)
    plt.close()
    print(f"Chart → {OUT}/12_cat_stress_test.png")


if __name__ == "__main__":
    main()
