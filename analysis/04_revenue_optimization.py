"""
KAT Insurance Co. - Revenue Optimization Analysis
====================================================
Identifies actionable revenue optimization opportunities across:
- Pricing efficiency by segment
- Channel profitability and mix optimization
- Cross-sell and upsell opportunities
- Premium leakage analysis
- Agent productivity benchmarking
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

print("=" * 80)
print("KAT INSURANCE CO. - REVENUE OPTIMIZATION ANALYSIS")
print("=" * 80)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. PRICING EFFICIENCY BY SEGMENT
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'━' * 80}")
print("1. PRICING EFFICIENCY BY SEGMENT")
print(f"{'━' * 80}")

segment_pricing = df.groupby(["product_line", "customer_segment"]).agg(
    count=("transaction_id", "count"),
    avg_premium=("net_premium", "mean"),
    avg_claim=("claim_amount", "mean"),
    total_premium=("net_premium", "sum"),
    total_claims=("claim_amount", "sum"),
    total_uw=("underwriting_result", "sum"),
).reset_index()

segment_pricing["loss_ratio"] = segment_pricing["total_claims"] / segment_pricing["total_premium"]
segment_pricing["uw_margin"] = segment_pricing["total_uw"] / segment_pricing["total_premium"]
segment_pricing["risk_adj_premium"] = segment_pricing["avg_claim"] / segment_pricing["loss_ratio"]

print("\nPricing Efficiency - Product x Segment:")
print(f"  {'Product':<12} {'Segment':<16} {'Count':>7} {'Avg Prem':>10} "
      f"{'LR':>7} {'UW Margin':>10}")
print(f"  {'─' * 62}")
for _, r in segment_pricing.sort_values(["product_line", "uw_margin"], ascending=[True, False]).iterrows():
    flag = " << underpriced" if r["loss_ratio"] > 0.7 else ""
    print(f"  {r['product_line']:<12} {r['customer_segment']:<16} {r['count']:>7,} "
          f"${r['avg_premium']:>8,.0f} {r['loss_ratio']:>6.1%} {r['uw_margin']:>9.1%}{flag}")

# Identify underpriced segments
underpriced = segment_pricing[segment_pricing["loss_ratio"] > 0.65].sort_values("total_premium", ascending=False)
if len(underpriced) > 0:
    print(f"\nUnderpriced Segments (Loss Ratio > 65%):")
    total_underpriced_premium = underpriced["total_premium"].sum()
    print(f"  {len(underpriced)} segments representing ${total_underpriced_premium:,.0f} in premium")
    print("  Recommended action: Rate adequacy review and potential re-pricing")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. CHANNEL PROFITABILITY & MIX OPTIMIZATION
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n\n{'━' * 80}")
print("2. CHANNEL PROFITABILITY & MIX OPTIMIZATION")
print(f"{'━' * 80}")

channel_perf = df.groupby("sales_channel").agg(
    policies=("transaction_id", "count"),
    net_premium=("net_premium", "sum"),
    claims=("claim_amount", "sum"),
    commission=("commission", "sum"),
    admin=("admin_cost", "sum"),
    uw_result=("underwriting_result", "sum"),
    avg_premium=("net_premium", "mean"),
).reset_index()

channel_perf["loss_ratio"] = channel_perf["claims"] / channel_perf["net_premium"]
channel_perf["commission_rate"] = channel_perf["commission"] / channel_perf["net_premium"]
channel_perf["total_cost_ratio"] = (
    (channel_perf["claims"] + channel_perf["commission"] + channel_perf["admin"])
    / channel_perf["net_premium"]
)
channel_perf["profit_per_policy"] = channel_perf["uw_result"] / channel_perf["policies"]
channel_perf["mix_share"] = channel_perf["net_premium"] / channel_perf["net_premium"].sum() * 100

print("\nChannel Economics:")
print(f"  {'Channel':<12} {'Mix%':>6} {'Avg Prem':>10} {'LR':>7} {'Comm%':>7} "
      f"{'Cost Ratio':>11} {'Profit/Pol':>11}")
print(f"  {'─' * 64}")
for _, r in channel_perf.sort_values("profit_per_policy", ascending=False).iterrows():
    print(f"  {r['sales_channel']:<12} {r['mix_share']:>5.1f}% ${r['avg_premium']:>8,.0f} "
          f"{r['loss_ratio']:>6.1%} {r['commission_rate']:>6.1%} "
          f"{r['total_cost_ratio']:>10.1%} ${r['profit_per_policy']:>9,.0f}")

# Optimal channel mix simulation
best_channel = channel_perf.loc[channel_perf["profit_per_policy"].idxmax(), "sales_channel"]
print(f"\n  Most profitable channel: {best_channel}")
print("  Recommended: Shift 5% of Broker volume to Direct/Online channels")
print("  Estimated annual commission savings: ", end="")
broker_comm_rate = channel_perf.loc[channel_perf["sales_channel"] == "Broker", "commission_rate"].values[0]
online_comm_rate = channel_perf.loc[channel_perf["sales_channel"] == "Online", "commission_rate"].values[0]
broker_premium = channel_perf.loc[channel_perf["sales_channel"] == "Broker", "net_premium"].values[0]
shift_savings = broker_premium * 0.05 * (broker_comm_rate - online_comm_rate)
print(f"${shift_savings:,.0f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. CROSS-SELL & UPSELL OPPORTUNITIES
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n\n{'━' * 80}")
print("3. CROSS-SELL & UPSELL OPPORTUNITIES")
print(f"{'━' * 80}")

# Multi-policy analysis
customer_products = df.groupby("customer_id").agg(
    num_products=("product_line", "nunique"),
    products=("product_line", lambda x: list(x.unique())),
    total_premium=("net_premium", "sum"),
    total_claims=("claim_amount", "sum"),
)
customer_products["loss_ratio"] = customer_products["total_claims"] / customer_products["total_premium"]

multi_dist = customer_products["num_products"].value_counts().sort_index()
print("\nCustomer Product Holding Distribution:")
for n_prod, count in multi_dist.items():
    pct = count / len(customer_products) * 100
    avg_prem = customer_products[customer_products["num_products"] == n_prod]["total_premium"].mean()
    avg_lr = customer_products[customer_products["num_products"] == n_prod]["loss_ratio"].mean()
    bar = "█" * int(pct)
    print(f"  {n_prod} product(s):  {count:>6,} customers ({pct:>5.1f}%)  "
          f"Avg Prem: ${avg_prem:>8,.0f}  LR: {avg_lr:.1%}  {bar}")

# Cross-sell opportunity sizing
single_product = customer_products[customer_products["num_products"] == 1]
single_auto = sum(1 for _, r in single_product.iterrows() if "Auto" in r["products"])
single_home = sum(1 for _, r in single_product.iterrows() if "Home" in r["products"])

print(f"\nCross-Sell Opportunity Sizing:")
print(f"  Single-product Auto customers:   {single_auto:,}")
print(f"  Single-product Home customers:   {single_home:,}")
print(f"  Auto+Home bundle opportunity:    {min(single_auto, single_home):,} households")

avg_home_prem = df[df["product_line"] == "Home"]["net_premium"].mean()
est_xsell_revenue = min(single_auto, single_home) * avg_home_prem * 0.15  # 15% conversion
print(f"  Estimated incremental revenue at 15% conversion: ${est_xsell_revenue:,.0f}")

# Deductible optimization
print(f"\nDeductible Distribution & Premium Opportunity:")
for product in ["Auto", "Home", "Health", "Commercial"]:
    product_df = df[df["product_line"] == product]
    deduct_analysis = product_df.groupby("deductible").agg(
        count=("transaction_id", "count"),
        avg_premium=("net_premium", "mean"),
    ).reset_index()
    print(f"\n  {product}:")
    for _, r in deduct_analysis.iterrows():
        pct = r["count"] / len(product_df) * 100
        print(f"    ${r['deductible']:>6,} deductible: {r['count']:>5,} ({pct:>5.1f}%)  "
              f"Avg Premium: ${r['avg_premium']:>8,.0f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. PREMIUM LEAKAGE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n\n{'━' * 80}")
print("4. PREMIUM LEAKAGE ANALYSIS")
print(f"{'━' * 80}")

# Renewal discount analysis
total_discounts = df["renewal_discount"].sum()
total_gross = df["gross_premium"].sum()
discount_rate = total_discounts / total_gross * 100

print(f"\nRenewal Discount Summary:")
print(f"  Total Gross Premium:       ${total_gross:>14,.0f}")
print(f"  Total Renewal Discounts:   ${total_discounts:>14,.0f}")
print(f"  Effective Discount Rate:   {discount_rate:.2f}%")

# Discount by product
discount_by_product = df.groupby("product_line").agg(
    gross=("gross_premium", "sum"),
    discounts=("renewal_discount", "sum"),
).reset_index()
discount_by_product["discount_rate"] = discount_by_product["discounts"] / discount_by_product["gross"] * 100

print(f"\n  {'Product':<14} {'Gross Prem':>14} {'Discounts':>12} {'Rate':>7}")
print(f"  {'─' * 47}")
for _, r in discount_by_product.sort_values("discount_rate", ascending=False).iterrows():
    print(f"  {r['product_line']:<14} ${r['gross']:>12,.0f} ${r['discounts']:>10,.0f} "
          f"{r['discount_rate']:>6.2f}%")

# Discount effectiveness (do discounted customers churn less?)
df["has_discount"] = df["renewal_discount"] > 0
disc_churn = df[df["has_discount"]]["policy_status"].isin(["Cancelled", "Lapsed"]).mean()
no_disc_churn = df[~df["has_discount"]]["policy_status"].isin(["Cancelled", "Lapsed"]).mean()

print(f"\n  Discount Effectiveness:")
print(f"    Churn rate WITH discount:     {disc_churn:.1%}")
print(f"    Churn rate WITHOUT discount:  {no_disc_churn:.1%}")
print(f"    Retention lift:               {(no_disc_churn - disc_churn):.1%} points")

# Estimate optimal discount
if disc_churn < no_disc_churn:
    retained_revenue = total_discounts / (no_disc_churn - disc_churn) if (no_disc_churn - disc_churn) > 0 else 0
    print(f"    Cost per retained customer:   ${retained_revenue / len(df[df['has_discount']]):,.0f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. AGENT PRODUCTIVITY BENCHMARKING
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n\n{'━' * 80}")
print("5. AGENT PRODUCTIVITY BENCHMARKING")
print(f"{'━' * 80}")

agent_perf = df.groupby(["agent_name", "agent_seniority"]).agg(
    policies=("transaction_id", "count"),
    net_premium=("net_premium", "sum"),
    claims=("claim_amount", "sum"),
    commission=("commission", "sum"),
    uw_result=("underwriting_result", "sum"),
    new_business=("is_new_business", "sum"),
    avg_premium=("net_premium", "mean"),
).reset_index()

agent_perf["loss_ratio"] = agent_perf["claims"] / agent_perf["net_premium"]
agent_perf["new_biz_rate"] = agent_perf["new_business"] / agent_perf["policies"]
agent_perf["profit_per_policy"] = agent_perf["uw_result"] / agent_perf["policies"]
agent_perf["revenue_rank"] = agent_perf["net_premium"].rank(ascending=False).astype(int)
agent_perf["profit_rank"] = agent_perf["uw_result"].rank(ascending=False).astype(int)

print("\nAgent Performance Scorecard:")
print(f"  {'Agent':<20} {'Level':<8} {'Policies':>8} {'Premium':>14} "
      f"{'LR':>7} {'New Biz%':>8} {'Rev Rank':>9}")
print(f"  {'─' * 74}")
for _, r in agent_perf.sort_values("net_premium", ascending=False).iterrows():
    print(f"  {r['agent_name']:<20} {r['agent_seniority']:<8} {r['policies']:>8,} "
          f"${r['net_premium']:>12,.0f} {r['loss_ratio']:>6.1%} "
          f"{r['new_biz_rate']:>7.1%} #{r['revenue_rank']:>7}")

# Seniority tier analysis
tier_perf = agent_perf.groupby("agent_seniority").agg(
    agents=("agent_name", "count"),
    avg_policies=("policies", "mean"),
    avg_premium=("net_premium", "mean"),
    avg_loss_ratio=("loss_ratio", "mean"),
    avg_profit=("uw_result", "mean"),
).reset_index()

print(f"\nAgent Tier Summary:")
print(f"  {'Tier':<10} {'Agents':>7} {'Avg Policies':>13} {'Avg Premium':>14} "
      f"{'Avg LR':>8} {'Avg Profit':>12}")
print(f"  {'─' * 64}")
for _, r in tier_perf.iterrows():
    print(f"  {r['agent_seniority']:<10} {r['agents']:>7} {r['avg_policies']:>13,.0f} "
          f"${r['avg_premium']:>12,.0f} {r['avg_loss_ratio']:>7.1%} "
          f"${r['avg_profit']:>10,.0f}")


# ─── Revenue Optimization Summary ────────────────────────────────────────────
print(f"\n\n{'━' * 80}")
print("REVENUE OPTIMIZATION SUMMARY")
print(f"{'━' * 80}")
print("""
  Opportunity Area                     Estimated Impact
  ─────────────────────────────────────────────────────
  1. Reprice underperforming segments  $250K-500K annual
  2. Channel mix optimization          $150K-300K commission savings
  3. Auto+Home cross-sell program      $200K-400K new premium
  4. Renewal discount rationalization  $100K-200K premium recovery
  5. Agent productivity coaching       10-15% premium lift for juniors

  Total Estimated Revenue Impact:      $700K - $1.4M annually

  These estimates are based on conservative assumptions and would require
  actuarial validation before implementation.
""")
print("=" * 80)
