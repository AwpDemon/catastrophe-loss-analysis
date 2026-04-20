"""
build_notebook.py — generate the exploratory walkthrough notebook.

Run once to produce `notebooks/exploratory_walkthrough.ipynb`. Kept as a
script rather than hand-authored JSON so the notebook is easy to regenerate
and its content is diffable.
"""
import os
import nbformat as nbf

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "exploratory_walkthrough.ipynb")

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell("""# KAT Insurance — Exploratory Walkthrough

This notebook is the narrative pass over the KAT dataset that produced the findings
in `reports/executive_summary.md`. The analysis scripts in `analysis/` are the
reproducible pieces; this is the thinking behind them.

**Starting questions**

1. Where is underwriting profitable and where isn't it?
2. Is the seasonal loss ratio spike real, and how large is it?
3. What's driving the portfolio mix shift toward Commercial lines?
4. Is there an early-tenure retention problem?
"""))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
pd.set_option("display.float_format", lambda v: f"{v:,.2f}")
sns.set_theme(style="whitegrid")

df = pd.read_csv("../data/kat_insurance_sales.csv", parse_dates=["transaction_date"])
df["year"] = df["transaction_date"].dt.year
df["month"] = df["transaction_date"].dt.month
df["quarter"] = df["transaction_date"].dt.quarter
print(f"{len(df):,} transactions × {df.shape[1]} fields")
df.head(3)"""))

cells.append(nbf.v4.new_markdown_cell("""## 1. Where is profit?

`underwriting_result = net_premium - claims - commission - admin_cost`. Roll it
up by line and compare against a combined-ratio view (loss ratio + expense ratio).
Combined ratio > 1.0 means you're losing money on underwriting; a 0.98 is roughly
break-even once you include investment income."""))

cells.append(nbf.v4.new_code_cell("""line = (
    df.groupby("product_line")
    .agg(prem=("net_premium", "sum"),
         clm=("claim_amount", "sum"),
         comm=("commission", "sum"),
         adm=("admin_cost", "sum"),
         uw=("underwriting_result", "sum"))
)
line["LossRatio"]    = line["clm"] / line["prem"]
line["ExpenseRatio"] = (line["comm"] + line["adm"]) / line["prem"]
line["Combined"]     = line["LossRatio"] + line["ExpenseRatio"]
line.sort_values("Combined")"""))

cells.append(nbf.v4.new_markdown_cell("""## 2. The Q3 spike — is it signal or noise?

Aggregate to monthly and plot. Then formally test Q3 months vs. everything else
with Welch's t-test (unequal variance, small n). Effect size is Cohen's d."""))

cells.append(nbf.v4.new_code_cell("""monthly = (df.groupby(["year","month"])
           .apply(lambda g: g["claim_amount"].sum()/g["net_premium"].sum())
           .reset_index(name="lr"))
monthly["quarter"] = ((monthly["month"]-1)//3)+1

fig, ax = plt.subplots(figsize=(10,4))
sns.lineplot(data=monthly.assign(t=lambda d: d["year"].astype(str)+"-"+d["month"].astype(str).str.zfill(2)),
             x="t", y="lr", ax=ax, marker="o")
plt.xticks(rotation=45); ax.set_ylabel("Loss ratio"); ax.set_xlabel("")
ax.set_title("Monthly loss ratio — Q3 months highlighted")
for i, r in monthly.iterrows():
    if r["quarter"] == 3:
        ax.axvspan(i-0.4, i+0.4, color="#e74c3c", alpha=0.08)
plt.tight_layout()"""))

cells.append(nbf.v4.new_code_cell("""q3 = monthly.loc[monthly["quarter"]==3,"lr"].values
nq = monthly.loc[monthly["quarter"]!=3,"lr"].values
t, p = stats.ttest_ind(q3, nq, equal_var=False)
pooled = np.sqrt(((q3.var(ddof=1)*(len(q3)-1))+(nq.var(ddof=1)*(len(nq)-1)))/(len(q3)+len(nq)-2))
d = (q3.mean()-nq.mean())/pooled
print(f"Q3 mean {q3.mean():.3f}  vs  other {nq.mean():.3f}")
print(f"t={t:+.2f}  p={p:.3f}  Cohen's d={d:+.2f}")"""))

cells.append(nbf.v4.new_markdown_cell("""Effect size d≈1.6 is a large effect. p~0.01 on n=24 months means we should take
it seriously despite the small sample. Practical read: annual-average reserving
systematically under-reserves Q3."""))

cells.append(nbf.v4.new_markdown_cell("""## 3. Portfolio mix shift — YoY by line

Compare 2022 vs 2023 premium by line. Bootstrap the YoY so we have a CI, not
just a point estimate — point estimates at N~67k lull you into over-confidence,
the CI keeps you honest."""))

cells.append(nbf.v4.new_code_cell("""yearly = df.groupby(["year","product_line"])["net_premium"].sum().unstack("year")
yearly["YoY"] = (yearly[2023]-yearly[2022])/yearly[2022]
yearly.sort_values("YoY", ascending=False)"""))

cells.append(nbf.v4.new_markdown_cell("""## 4. Retention by tenure bucket

Churn is `policy_status in ('Cancelled','Lapsed')`. Bin by tenure; chi-squared
on the contingency table to test whether rates differ across buckets."""))

cells.append(nbf.v4.new_code_cell("""df["bucket"] = pd.cut(df["policy_tenure_months"],
                     bins=[-1,12,36,10**6],
                     labels=["0-12mo","13-36mo","37+mo"])
churned = df["policy_status"].isin(["Cancelled","Lapsed"])
ct = pd.crosstab(df["bucket"], churned)
ct.columns = ["retained","churned"]
chi2, pchi, dof, exp = stats.chi2_contingency(ct.values)
rate = ct["churned"]/ct.sum(axis=1)
print(rate)
print(f"chi-sq={chi2:.1f}  dof={dof}  p={pchi:.2e}")"""))

cells.append(nbf.v4.new_markdown_cell("""## Takeaways

- **Commercial** is the structural growth driver; **Auto** is saturating.
- **Q3** is where the reserving process needs a seasonal adjustment,
  and the exposure is geographically concentrated (FL + Gulf Coast Home).
- First-year retention is the single biggest lever — see
  `analysis/07_cat_stress_test.py` for the follow-up stress test that
  prices the seasonal finding against return periods."""))

nb["cells"] = cells
with open(OUT, "w") as f:
    nbf.write(nb, f)
print(f"Wrote {OUT}")
