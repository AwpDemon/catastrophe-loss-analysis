"""
KAT Insurance Co. - Visualization Generator
==============================================
Generates all charts and visualizations for the analytics project.
Outputs PNG files to the visualizations/ directory.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import sys
import warnings

warnings.filterwarnings("ignore")

# ─── Configuration ───────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "kat_insurance_sales.csv")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(DATA_PATH):
    print("ERROR: Dataset not found. Run 'python data/generate_sales_data.py' first.")
    sys.exit(1)

# Style
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({
    "figure.figsize": (12, 7),
    "figure.dpi": 150,
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "font.size": 10,
    "figure.facecolor": "white",
})

COLORS = {
    "Auto": "#2196F3",
    "Home": "#4CAF50",
    "Life": "#9C27B0",
    "Health": "#FF9800",
    "Commercial": "#F44336",
}

df = pd.read_csv(DATA_PATH, parse_dates=["transaction_date"])
df["year"] = df["transaction_date"].dt.year
df["quarter"] = df["transaction_date"].dt.quarter
df["month"] = df["transaction_date"].dt.month
df["year_month"] = df["transaction_date"].dt.to_period("M")
df["year_quarter"] = df["year"].astype(str) + "-Q" + df["quarter"].astype(str)

print("=" * 60)
print("Generating visualizations...")
print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 1: Premium Revenue by Product Line (YoY Comparison)
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(12, 7))
annual = df.groupby(["year", "product_line"])["net_premium"].sum().unstack()
x = np.arange(len(annual.columns))
width = 0.35

bars1 = ax.bar(x - width/2, annual.loc[2022] / 1e6, width, label="2022",
               color=[COLORS[c] for c in annual.columns], alpha=0.6, edgecolor="white")
bars2 = ax.bar(x + width/2, annual.loc[2023] / 1e6, width, label="2023",
               color=[COLORS[c] for c in annual.columns], alpha=1.0, edgecolor="white")

ax.set_xlabel("Product Line")
ax.set_ylabel("Net Premium ($M)")
ax.set_title("Premium Revenue by Product Line - YoY Comparison (2022 vs 2023)")
ax.set_xticks(x)
ax.set_xticklabels(annual.columns)
ax.legend()
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}M"))

for bar in bars2:
    height = bar.get_height()
    ax.annotate(f"${height:.1f}M", xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "01_premium_yoy_comparison.png"))
plt.close()
print("  [1/10] Premium YoY comparison")


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 2: Monthly Loss Ratio Trend
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(14, 7))
monthly = df.groupby("year_month").agg(
    premium=("net_premium", "sum"), claims=("claim_amount", "sum")
).reset_index()
monthly["loss_ratio"] = monthly["claims"] / monthly["premium"]
monthly["period_str"] = monthly["year_month"].astype(str)

ax.plot(range(len(monthly)), monthly["loss_ratio"], color="#1565C0", linewidth=2.5,
        marker="o", markersize=5, zorder=5)
ax.fill_between(range(len(monthly)), monthly["loss_ratio"], alpha=0.15, color="#1565C0")
ax.axhline(y=monthly["loss_ratio"].mean(), color="#E53935", linestyle="--",
           linewidth=1.5, label=f"Average: {monthly['loss_ratio'].mean():.1%}")

# Highlight Q3 months
for i, row in monthly.iterrows():
    period = str(row["year_month"])
    month_num = int(period.split("-")[1])
    if month_num in [7, 8, 9]:
        ax.axvspan(i - 0.5, i + 0.5, alpha=0.1, color="red")

ax.set_xlabel("Month")
ax.set_ylabel("Loss Ratio")
ax.set_title("Monthly Loss Ratio Trend (2022-2023) - Q3 Hurricane Season Highlighted")
ax.set_xticks(range(0, len(monthly), 2))
ax.set_xticklabels([monthly["period_str"].iloc[i] for i in range(0, len(monthly), 2)],
                   rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "02_monthly_loss_ratio_trend.png"))
plt.close()
print("  [2/10] Monthly loss ratio trend")


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 3: Regional Performance Heatmap
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(14, 8))
regional = df.groupby(["region", "product_line"])["underwriting_result"].sum().unstack(fill_value=0) / 1e3
sns.heatmap(regional, annot=True, fmt=".0f", cmap="RdYlGn", center=0,
            linewidths=0.5, ax=ax, cbar_kws={"label": "UW Result ($K)"})
ax.set_title("Underwriting Result by Region x Product Line ($K)")
ax.set_xlabel("Product Line")
ax.set_ylabel("Region")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "03_regional_performance_heatmap.png"))
plt.close()
print("  [3/10] Regional performance heatmap")


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 4: Product Mix Shift (Stacked Area)
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(14, 7))
monthly_mix = df.groupby(["year_month", "product_line"])["net_premium"].sum().unstack(fill_value=0)
monthly_mix_pct = monthly_mix.div(monthly_mix.sum(axis=1), axis=0)

# Convert period index to sequential integers for plotting
x_range = range(len(monthly_mix_pct))
labels = [str(p) for p in monthly_mix_pct.index]

ax.stackplot(x_range,
             [monthly_mix_pct[col].values for col in monthly_mix_pct.columns],
             labels=monthly_mix_pct.columns,
             colors=[COLORS[c] for c in monthly_mix_pct.columns],
             alpha=0.8)

ax.set_xlabel("Month")
ax.set_ylabel("Share of Net Premium")
ax.set_title("Product Mix Evolution (% of Total Net Premium)")
ax.set_xticks(range(0, len(labels), 3))
ax.set_xticklabels([labels[i] for i in range(0, len(labels), 3)], rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "04_product_mix_evolution.png"))
plt.close()
print("  [4/10] Product mix evolution")


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 5: Customer Retention by Tenure
# ═══════════════════════════════════════════════════════════════════════════════

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# Churn rate by tenure bucket
df["tenure_bucket"] = pd.cut(df["policy_tenure_months"],
                             bins=[-1, 6, 12, 24, 36, 200],
                             labels=["0-6mo", "7-12mo", "13-24mo", "25-36mo", "36+mo"])

churn = df.groupby("tenure_bucket", observed=True).apply(
    lambda x: x["policy_status"].isin(["Cancelled", "Lapsed"]).mean(), include_groups=False
)

ax1.bar(range(len(churn)), churn.values, color=["#F44336", "#FF7043", "#FFA726", "#66BB6A", "#43A047"])
ax1.set_xticks(range(len(churn)))
ax1.set_xticklabels(churn.index)
ax1.set_xlabel("Policy Tenure")
ax1.set_ylabel("Churn Rate")
ax1.set_title("Churn Rate by Policy Tenure")
ax1.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

for i, v in enumerate(churn.values):
    ax1.text(i, v + 0.003, f"{v:.1%}", ha="center", fontsize=10, fontweight="bold")

# Churn by product
churn_product = df.groupby("product_line").apply(
    lambda x: x["policy_status"].isin(["Cancelled", "Lapsed"]).mean(), include_groups=False
).sort_values(ascending=True)

bars = ax2.barh(range(len(churn_product)), churn_product.values,
                color=[COLORS[p] for p in churn_product.index])
ax2.set_yticks(range(len(churn_product)))
ax2.set_yticklabels(churn_product.index)
ax2.set_xlabel("Churn Rate")
ax2.set_title("Churn Rate by Product Line")
ax2.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))

for i, v in enumerate(churn_product.values):
    ax2.text(v + 0.002, i, f"{v:.1%}", va="center", fontsize=10)

plt.suptitle("Customer Retention Analysis", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "05_customer_retention.png"), bbox_inches="tight")
plt.close()
print("  [5/10] Customer retention analysis")


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 6: Combined Ratio Waterfall
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(12, 7))

total_net = df["net_premium"].sum()
lr = df["claim_amount"].sum() / total_net
cr = df["commission"].sum() / total_net
ar = df["admin_cost"].sum() / total_net
combined = lr + cr + ar
uw_margin = 1 - combined

categories = ["Loss Ratio", "Commission", "Admin Cost", "Combined Ratio", "UW Margin"]
values = [lr, cr, ar, combined, uw_margin]
colors_wf = ["#E53935", "#FF9800", "#FFC107", "#1565C0", "#43A047"]

bars = ax.bar(categories, values, color=colors_wf, edgecolor="white", linewidth=1.5)
ax.axhline(y=1.0, color="black", linestyle="-", linewidth=0.5, alpha=0.3)

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{val:.1%}", ha="center", va="bottom", fontsize=12, fontweight="bold")

ax.set_ylabel("Ratio")
ax.set_title("Combined Ratio Decomposition - Portfolio Level")
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "06_combined_ratio_waterfall.png"))
plt.close()
print("  [6/10] Combined ratio waterfall")


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 7: Channel Performance Comparison
# ═══════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(16, 6))

channel_data = df.groupby("sales_channel").agg(
    premium=("net_premium", "sum"),
    claims=("claim_amount", "sum"),
    commission=("commission", "sum"),
    policies=("transaction_id", "count"),
    uw_result=("underwriting_result", "sum"),
).reset_index()
channel_data["loss_ratio"] = channel_data["claims"] / channel_data["premium"]
channel_data["profit_per_policy"] = channel_data["uw_result"] / channel_data["policies"]

ch_colors = ["#1565C0", "#43A047", "#FF9800", "#9C27B0"]

# Premium volume
axes[0].bar(channel_data["sales_channel"], channel_data["premium"] / 1e6, color=ch_colors)
axes[0].set_title("Premium Volume ($M)")
axes[0].set_ylabel("$M")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))

# Loss ratio
axes[1].bar(channel_data["sales_channel"], channel_data["loss_ratio"], color=ch_colors)
axes[1].set_title("Loss Ratio by Channel")
axes[1].yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

# Profit per policy
axes[2].bar(channel_data["sales_channel"], channel_data["profit_per_policy"], color=ch_colors)
axes[2].set_title("Profit per Policy ($)")
axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.suptitle("Sales Channel Performance Comparison", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "07_channel_performance.png"))
plt.close()
print("  [7/10] Channel performance comparison")


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 8: Quarterly Premium Trend by Product
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(14, 7))
qtr_data = df.groupby(["year_quarter", "product_line"])["net_premium"].sum().unstack()
quarters = sorted(df["year_quarter"].unique())

for product in qtr_data.columns:
    ax.plot(range(len(quarters)), qtr_data[product].values / 1e6,
            marker="o", linewidth=2.5, label=product, color=COLORS[product], markersize=6)

ax.set_xlabel("Quarter")
ax.set_ylabel("Net Premium ($M)")
ax.set_title("Quarterly Premium Trend by Product Line (2022-2023)")
ax.set_xticks(range(len(quarters)))
ax.set_xticklabels(quarters, rotation=45)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}M"))
ax.legend(title="Product Line")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "08_quarterly_premium_trend.png"))
plt.close()
print("  [8/10] Quarterly premium trend")


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 9: Claims Severity Distribution
# ═══════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

for i, product in enumerate(["Auto", "Home", "Life", "Health", "Commercial"]):
    pf = df[(df["product_line"] == product) & (df["claim_amount"] > 0)]
    if len(pf) > 0:
        axes[i].hist(pf["claim_amount"], bins=50, color=COLORS[product],
                     alpha=0.7, edgecolor="white")
        axes[i].axvline(pf["claim_amount"].mean(), color="red", linestyle="--",
                       label=f"Mean: ${pf['claim_amount'].mean():,.0f}")
        axes[i].axvline(pf["claim_amount"].median(), color="black", linestyle=":",
                       label=f"Median: ${pf['claim_amount'].median():,.0f}")
        axes[i].set_title(f"{product} Claims Distribution")
        axes[i].set_xlabel("Claim Amount ($)")
        axes[i].set_ylabel("Frequency")
        axes[i].legend(fontsize=8)
        axes[i].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))

axes[5].axis("off")
plt.suptitle("Claims Severity Distribution by Product Line", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "09_claims_distribution.png"))
plt.close()
print("  [9/10] Claims severity distribution")


# ═══════════════════════════════════════════════════════════════════════════════
# Chart 10: Agent Performance Scatter
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(12, 8))
agent_data = df.groupby(["agent_name", "agent_seniority"]).agg(
    premium=("net_premium", "sum"),
    policies=("transaction_id", "count"),
    claims=("claim_amount", "sum"),
    uw_result=("underwriting_result", "sum"),
).reset_index()
agent_data["loss_ratio"] = agent_data["claims"] / agent_data["premium"]

seniority_colors = {"Senior": "#1565C0", "Mid": "#FF9800", "Junior": "#43A047"}
seniority_sizes = {"Senior": 200, "Mid": 150, "Junior": 100}

for seniority in ["Senior", "Mid", "Junior"]:
    mask = agent_data["agent_seniority"] == seniority
    ax.scatter(agent_data.loc[mask, "premium"] / 1e6,
               agent_data.loc[mask, "loss_ratio"],
               s=seniority_sizes[seniority],
               color=seniority_colors[seniority],
               alpha=0.8, label=seniority, edgecolors="white", linewidth=1.5)
    for _, r in agent_data[mask].iterrows():
        ax.annotate(r["agent_name"].split()[-1],
                    (r["premium"] / 1e6, r["loss_ratio"]),
                    xytext=(5, 5), textcoords="offset points", fontsize=8)

ax.set_xlabel("Total Premium Volume ($M)")
ax.set_ylabel("Loss Ratio")
ax.set_title("Agent Performance: Premium Volume vs. Loss Ratio")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}M"))
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax.legend(title="Seniority")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "10_agent_performance.png"))
plt.close()
print("  [10/10] Agent performance scatter")


print(f"\n{'=' * 60}")
print(f"All 10 visualizations saved to: {OUTPUT_DIR}/")
print("=" * 60)
