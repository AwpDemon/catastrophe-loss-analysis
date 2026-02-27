"""
KAT Insurance Co. - Data Overview & Profiling
===============================================
Initial data quality assessment and profiling of the 65K+ transaction dataset.
Mirrors the Excel Data > Get Info and initial summary statistics workflow.
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

print("=" * 70)
print("KAT INSURANCE CO. - DATA OVERVIEW & PROFILING")
print("=" * 70)

# ─── 1. Shape & Structure ────────────────────────────────────────────────────
print(f"\n{'─' * 70}")
print("1. DATASET DIMENSIONS")
print(f"{'─' * 70}")
print(f"  Records:  {len(df):,}")
print(f"  Fields:   {len(df.columns)}")
print(f"  Memory:   {df.memory_usage(deep=True).sum() / (1024**2):.1f} MB")

# ─── 2. Date Range ───────────────────────────────────────────────────────────
print(f"\n{'─' * 70}")
print("2. DATE RANGE")
print(f"{'─' * 70}")
print(f"  Earliest: {df['transaction_date'].min().strftime('%Y-%m-%d')}")
print(f"  Latest:   {df['transaction_date'].max().strftime('%Y-%m-%d')}")
print(f"  Span:     {(df['transaction_date'].max() - df['transaction_date'].min()).days} days")

# ─── 3. Data Types ───────────────────────────────────────────────────────────
print(f"\n{'─' * 70}")
print("3. DATA TYPES")
print(f"{'─' * 70}")
for col in df.columns:
    null_count = df[col].isnull().sum()
    null_str = f"  ({null_count} nulls)" if null_count > 0 else ""
    print(f"  {col:<28} {str(df[col].dtype):<12} {null_str}")

# ─── 4. Missing Values ───────────────────────────────────────────────────────
print(f"\n{'─' * 70}")
print("4. MISSING VALUE SUMMARY")
print(f"{'─' * 70}")
missing = df.isnull().sum()
total_missing = missing.sum()
if total_missing == 0:
    print("  No missing values detected across all fields.")
else:
    for col, count in missing[missing > 0].items():
        pct = count / len(df) * 100
        print(f"  {col:<28} {count:>6,} ({pct:.2f}%)")

# ─── 5. Numeric Summary ──────────────────────────────────────────────────────
print(f"\n{'─' * 70}")
print("5. NUMERIC FIELD STATISTICS")
print(f"{'─' * 70}")
numeric_cols = ["gross_premium", "renewal_discount", "net_premium", "deductible",
                "claim_amount", "num_claims", "commission", "admin_cost",
                "loss_ratio", "underwriting_result", "policy_tenure_months"]

for col in numeric_cols:
    stats = df[col].describe()
    print(f"\n  {col}:")
    print(f"    Mean:   {stats['mean']:>12,.2f}    Std:  {stats['std']:>12,.2f}")
    print(f"    Min:    {stats['min']:>12,.2f}    Max:  {stats['max']:>12,.2f}")
    print(f"    25th:   {stats['25%']:>12,.2f}    75th: {stats['75%']:>12,.2f}")
    print(f"    Median: {stats['50%']:>12,.2f}")

# ─── 6. Categorical Summary ──────────────────────────────────────────────────
print(f"\n{'─' * 70}")
print("6. CATEGORICAL FIELD DISTRIBUTIONS")
print(f"{'─' * 70}")
cat_cols = ["product_line", "region", "state", "agent_seniority",
            "sales_channel", "customer_segment", "customer_age_bracket",
            "customer_gender", "payment_frequency", "policy_status"]

for col in cat_cols:
    print(f"\n  {col} ({df[col].nunique()} unique values):")
    for val, count in df[col].value_counts().head(10).items():
        pct = count / len(df) * 100
        bar = "█" * int(pct / 2)
        print(f"    {str(val):<20} {count:>6,} ({pct:>5.1f}%) {bar}")

# ─── 7. Key Aggregates ───────────────────────────────────────────────────────
print(f"\n{'─' * 70}")
print("7. KEY BUSINESS METRICS (PORTFOLIO LEVEL)")
print(f"{'─' * 70}")

total_gross = df["gross_premium"].sum()
total_net = df["net_premium"].sum()
total_claims = df["claim_amount"].sum()
total_commission = df["commission"].sum()
total_admin = df["admin_cost"].sum()
total_uw = df["underwriting_result"].sum()

overall_loss_ratio = total_claims / total_net
expense_ratio = (total_commission + total_admin) / total_net
combined_ratio = overall_loss_ratio + expense_ratio

print(f"  Total Gross Premium:      ${total_gross:>14,.2f}")
print(f"  Total Renewal Discounts:  ${df['renewal_discount'].sum():>14,.2f}")
print(f"  Total Net Premium:        ${total_net:>14,.2f}")
print(f"  Total Claims Paid:        ${total_claims:>14,.2f}")
print(f"  Total Commissions:        ${total_commission:>14,.2f}")
print(f"  Total Admin Costs:        ${total_admin:>14,.2f}")
print(f"  Total UW Result:          ${total_uw:>14,.2f}")
print(f"  ")
print(f"  Loss Ratio:               {overall_loss_ratio:>13.2%}")
print(f"  Expense Ratio:            {expense_ratio:>13.2%}")
print(f"  Combined Ratio:           {combined_ratio:>13.2%}")
print(f"  Underwriting Margin:      {1 - combined_ratio:>13.2%}")
print(f"  ")
print(f"  Unique Customers:         {df['customer_id'].nunique():>13,}")
print(f"  Unique Policies:          {df['policy_number'].nunique():>13,}")
print(f"  Avg Premium per Policy:   ${df['net_premium'].mean():>13,.2f}")
print(f"  New Business %:           {df['is_new_business'].mean():>13.2%}")

# ─── 8. Monthly Volume ───────────────────────────────────────────────────────
print(f"\n{'─' * 70}")
print("8. MONTHLY TRANSACTION VOLUME")
print(f"{'─' * 70}")

df["year_month"] = df["transaction_date"].dt.to_period("M")
monthly = df.groupby("year_month").agg(
    transactions=("transaction_id", "count"),
    net_premium=("net_premium", "sum"),
    claims=("claim_amount", "sum"),
).reset_index()

for _, row in monthly.iterrows():
    lr = row["claims"] / row["net_premium"] if row["net_premium"] > 0 else 0
    bar = "█" * int(row["transactions"] / 100)
    print(f"  {row['year_month']}  {row['transactions']:>5,} txns  "
          f"${row['net_premium']:>12,.0f} prem  "
          f"LR: {lr:.1%}  {bar}")

# ─── 9. Data Quality Flags ───────────────────────────────────────────────────
print(f"\n{'─' * 70}")
print("9. DATA QUALITY FLAGS")
print(f"{'─' * 70}")

negative_premiums = (df["net_premium"] < 0).sum()
extreme_loss = (df["loss_ratio"] > 10).sum()
zero_premium = (df["net_premium"] == 0).sum()
future_dates = (df["transaction_date"] > pd.Timestamp.now()).sum()

print(f"  Negative net premiums:    {negative_premiums:>6}")
print(f"  Extreme loss ratios >10x: {extreme_loss:>6}")
print(f"  Zero net premium:         {zero_premium:>6}")
print(f"  Future-dated records:     {future_dates:>6}")

if negative_premiums + extreme_loss + zero_premium + future_dates == 0:
    print("  >> No critical data quality issues detected.")
else:
    print("  >> Review flagged records before final analysis.")

print(f"\n{'=' * 70}")
print("Data profiling complete.")
print("=" * 70)
