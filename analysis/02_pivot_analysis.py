"""
KAT Insurance Co. - PivotTable-Equivalent Analysis
=====================================================
Replicates the Excel PivotTable analyses in pandas, including:
- Multi-dimensional cross-tabulations
- Calculated fields (Loss Ratio, Expense Ratio, Combined Ratio)
- Drill-down by Product Line, Region, Channel, Time Period
"""

import pandas as pd
import numpy as np
import os
import sys

# ─── Load Data ───────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "kat_insurance_sales.csv")

if not os.path.exists(DATA_PATH):
    print("ERROR: Dataset not found. Run 'python data/generate_sales_data.py' first.")
    sys.exit(1)

df = pd.read_csv(DATA_PATH, parse_dates=["transaction_date"])
df["year"] = df["transaction_date"].dt.year
df["quarter"] = df["transaction_date"].dt.quarter
df["month"] = df["transaction_date"].dt.month
df["year_quarter"] = df["year"].astype(str) + "-Q" + df["quarter"].astype(str)

print("=" * 80)
print("KAT INSURANCE CO. - PIVOT TABLE ANALYSIS")
print("=" * 80)

# ─── Helper: Calculated Fields ───────────────────────────────────────────────
def calc_metrics(group):
    """Calculate insurance KPIs matching Excel calculated fields."""
    net_prem = group["net_premium"].sum()
    claims = group["claim_amount"].sum()
    comm = group["commission"].sum()
    admin = group["admin_cost"].sum()
    uw = group["underwriting_result"].sum()

    loss_ratio = claims / net_prem if net_prem > 0 else 0
    expense_ratio = (comm + admin) / net_prem if net_prem > 0 else 0
    combined_ratio = loss_ratio + expense_ratio

    return pd.Series({
        "policies": len(group),
        "net_premium": net_prem,
        "claims": claims,
        "commission": comm,
        "admin_cost": admin,
        "uw_result": uw,
        "loss_ratio": loss_ratio,
        "expense_ratio": expense_ratio,
        "combined_ratio": combined_ratio,
        "uw_margin": 1 - combined_ratio,
        "avg_premium": group["net_premium"].mean(),
        "avg_claim": group.loc[group["claim_amount"] > 0, "claim_amount"].mean()
            if (group["claim_amount"] > 0).any() else 0,
        "claim_frequency": (group["claim_amount"] > 0).mean(),
    })


def print_pivot(title, pivot_df, value_fmt=None):
    """Pretty-print a pivot result."""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}")
    pd.set_option("display.max_columns", 15)
    pd.set_option("display.width", 120)
    pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
    print(pivot_df.to_string())
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 1: Product Line Summary (Rows: Product Line)
# Excel equivalent: Rows=Product_Line, Values=Sum of Net Premium, Sum of Claims,
#                   Calculated Field: Loss Ratio, Combined Ratio
# ═══════════════════════════════════════════════════════════════════════════════

pivot1 = df.groupby("product_line").apply(calc_metrics, include_groups=False).sort_values("net_premium", ascending=False)
print_pivot("PIVOT 1: Product Line Performance Summary", pivot1)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 2: Product Line x Year (Rows: Product, Columns: Year)
# Excel equivalent: Rows=Product_Line, Columns=Year, Values=Sum of Net Premium
# ═══════════════════════════════════════════════════════════════════════════════

pivot2_premium = pd.pivot_table(df, values="net_premium", index="product_line",
                                columns="year", aggfunc="sum", margins=True)
print_pivot("PIVOT 2: Net Premium by Product Line x Year", pivot2_premium)

pivot2_claims = pd.pivot_table(df, values="claim_amount", index="product_line",
                               columns="year", aggfunc="sum", margins=True)
print_pivot("PIVOT 2b: Claims by Product Line x Year", pivot2_claims)

# YoY Growth
if 2022 in pivot2_premium.columns and 2023 in pivot2_premium.columns:
    yoy_growth = ((pivot2_premium[2023] - pivot2_premium[2022]) / pivot2_premium[2022] * 100)
    print_pivot("PIVOT 2c: YoY Premium Growth % by Product Line",
                yoy_growth.to_frame("yoy_growth_%"))

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 3: Region Summary (Rows: Region)
# ═══════════════════════════════════════════════════════════════════════════════

pivot3 = df.groupby("region").apply(calc_metrics, include_groups=False).sort_values("net_premium", ascending=False)
print_pivot("PIVOT 3: Regional Performance Summary", pivot3)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 4: Region x Product Line (Matrix)
# Excel equivalent: Rows=Region, Columns=Product_Line, Values=Sum of Net Premium
# ═══════════════════════════════════════════════════════════════════════════════

pivot4 = pd.pivot_table(df, values="net_premium", index="region",
                        columns="product_line", aggfunc="sum", margins=True)
print_pivot("PIVOT 4: Net Premium - Region x Product Line Matrix", pivot4)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 5: Sales Channel Analysis
# ═══════════════════════════════════════════════════════════════════════════════

pivot5 = df.groupby("sales_channel").apply(calc_metrics, include_groups=False).sort_values("net_premium", ascending=False)
print_pivot("PIVOT 5: Sales Channel Performance", pivot5)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 6: Quarterly Trends (Rows: Year-Quarter)
# Excel equivalent: Rows=Year-Quarter, Values=Sum of Net Premium, Count of Policies,
#                   Calculated Field: Loss Ratio
# ═══════════════════════════════════════════════════════════════════════════════

pivot6 = df.groupby("year_quarter").apply(calc_metrics, include_groups=False)
print_pivot("PIVOT 6: Quarterly Performance Trends", pivot6)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 7: Agent Seniority x Product Line
# ═══════════════════════════════════════════════════════════════════════════════

pivot7 = pd.pivot_table(df, values=["net_premium", "commission"],
                        index="agent_seniority", columns="product_line",
                        aggfunc="sum")
print_pivot("PIVOT 7: Agent Seniority x Product Line (Premium & Commission)", pivot7)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 8: Customer Segment Analysis
# ═══════════════════════════════════════════════════════════════════════════════

pivot8 = df.groupby("customer_segment").apply(calc_metrics, include_groups=False).sort_values("net_premium", ascending=False)
print_pivot("PIVOT 8: Customer Segment Performance", pivot8)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 9: Age Bracket x Product Line
# ═══════════════════════════════════════════════════════════════════════════════

pivot9 = pd.pivot_table(df, values="net_premium", index="customer_age_bracket",
                        columns="product_line", aggfunc=["sum", "count"])
print_pivot("PIVOT 9: Customer Age Bracket x Product Line (Premium & Count)", pivot9)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 10: Policy Status Breakdown
# ═══════════════════════════════════════════════════════════════════════════════

pivot10 = df.groupby(["product_line", "policy_status"]).agg(
    count=("transaction_id", "count"),
    net_premium=("net_premium", "sum"),
    claims=("claim_amount", "sum"),
).reset_index()

pivot10_ct = pd.pivot_table(pivot10, values="count", index="product_line",
                            columns="policy_status", aggfunc="sum", fill_value=0, margins=True)
print_pivot("PIVOT 10: Policy Status by Product Line (Count)", pivot10_ct)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 11: Payment Frequency x Channel
# ═══════════════════════════════════════════════════════════════════════════════

pivot11 = pd.pivot_table(df, values="net_premium", index="payment_frequency",
                         columns="sales_channel", aggfunc=["sum", "mean"], margins=True)
print_pivot("PIVOT 11: Payment Frequency x Sales Channel", pivot11)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 12: Top Agents by Premium Volume
# ═══════════════════════════════════════════════════════════════════════════════

pivot12 = df.groupby(["agent_name", "agent_seniority"]).apply(calc_metrics, include_groups=False).sort_values(
    "net_premium", ascending=False
)
print_pivot("PIVOT 12: Agent Performance Ranking", pivot12)

# ═══════════════════════════════════════════════════════════════════════════════
# PIVOT 13: Loss Ratio Heatmap - Region x Quarter
# Excel equivalent: Conditional formatting on calculated Loss Ratio field
# ═══════════════════════════════════════════════════════════════════════════════

def lr_calc(g):
    net = g["net_premium"].sum()
    cl = g["claim_amount"].sum()
    return cl / net if net > 0 else 0

pivot13 = df.groupby(["region", "year_quarter"]).apply(lr_calc, include_groups=False).unstack(fill_value=0)
print_pivot("PIVOT 13: Loss Ratio Heatmap - Region x Quarter", pivot13)

# ─── Summary ──────────────────────────────────────────────────────────────────
print("=" * 80)
print("Pivot analysis complete. 13 pivot tables generated.")
print("These replicate the Excel PivotTable configurations documented in")
print("excel_templates/pivot_table_guide.md")
print("=" * 80)
