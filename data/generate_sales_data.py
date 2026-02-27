"""
KAT Insurance Co. - Synthetic Sales Data Generator
====================================================
Generates 65,000+ realistic insurance sales transactions spanning
January 2022 through December 2023, mirroring the production data
schema used in the original Excel-based analysis.

Outputs: data/kat_insurance_sales.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import warnings

warnings.filterwarnings("ignore")

# ─── Configuration ───────────────────────────────────────────────────────────
np.random.seed(42)
NUM_RECORDS = 67_500  # Target: 65K+
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "kat_insurance_sales.csv")

# ─── Reference Data ──────────────────────────────────────────────────────────

PRODUCT_LINES = {
    "Auto": {
        "weight": 0.32,
        "premium_range": (600, 3200),
        "premium_mean": 1450,
        "premium_std": 520,
        "deductible_options": [250, 500, 1000, 1500, 2000],
        "claim_probability": 0.18,
        "claim_severity_mean": 4200,
        "claim_severity_std": 3500,
        "growth_rate_2023": 0.04,
    },
    "Home": {
        "weight": 0.26,
        "premium_range": (800, 5500),
        "premium_mean": 2100,
        "premium_std": 850,
        "deductible_options": [500, 1000, 2000, 2500, 5000],
        "claim_probability": 0.12,
        "claim_severity_mean": 8500,
        "claim_severity_std": 7200,
        "growth_rate_2023": 0.06,
    },
    "Life": {
        "weight": 0.14,
        "premium_range": (300, 4000),
        "premium_mean": 1200,
        "premium_std": 680,
        "deductible_options": [0],
        "claim_probability": 0.02,
        "claim_severity_mean": 75000,
        "claim_severity_std": 45000,
        "growth_rate_2023": 0.03,
    },
    "Health": {
        "weight": 0.16,
        "premium_range": (2000, 12000),
        "premium_mean": 5200,
        "premium_std": 2100,
        "deductible_options": [500, 1000, 2000, 3000, 5000, 6500],
        "claim_probability": 0.35,
        "claim_severity_mean": 3800,
        "claim_severity_std": 5500,
        "growth_rate_2023": 0.08,
    },
    "Commercial": {
        "weight": 0.12,
        "premium_range": (2500, 25000),
        "premium_mean": 8500,
        "premium_std": 4800,
        "deductible_options": [1000, 2500, 5000, 10000],
        "claim_probability": 0.15,
        "claim_severity_mean": 15000,
        "claim_severity_std": 12000,
        "growth_rate_2023": 0.12,
    },
}

REGIONS = {
    "Atlanta Metro": {"states": ["GA"], "weight": 0.22, "performance_factor": 1.15},
    "Florida": {"states": ["FL"], "weight": 0.18, "performance_factor": 1.05},
    "Carolinas": {"states": ["NC", "SC"], "weight": 0.14, "performance_factor": 0.95},
    "Tennessee Valley": {"states": ["TN", "AL"], "weight": 0.12, "performance_factor": 0.90},
    "Gulf Coast": {"states": ["MS", "LA"], "weight": 0.10, "performance_factor": 0.85},
    "Virginia": {"states": ["VA"], "weight": 0.10, "performance_factor": 1.00},
    "Kentucky": {"states": ["KY"], "weight": 0.07, "performance_factor": 0.88},
    "Arkansas": {"states": ["AR"], "weight": 0.07, "performance_factor": 0.82},
}

AGENTS = [
    {"name": "Sarah Mitchell", "id": "AGT-001", "seniority": "Senior", "hire_year": 2015},
    {"name": "James Carter", "id": "AGT-002", "seniority": "Senior", "hire_year": 2016},
    {"name": "Maria Rodriguez", "id": "AGT-003", "seniority": "Senior", "hire_year": 2014},
    {"name": "David Kim", "id": "AGT-004", "seniority": "Mid", "hire_year": 2018},
    {"name": "Rachel Thompson", "id": "AGT-005", "seniority": "Mid", "hire_year": 2019},
    {"name": "Michael Johnson", "id": "AGT-006", "seniority": "Mid", "hire_year": 2019},
    {"name": "Emily Chen", "id": "AGT-007", "seniority": "Mid", "hire_year": 2020},
    {"name": "Robert Davis", "id": "AGT-008", "seniority": "Junior", "hire_year": 2021},
    {"name": "Ashley Williams", "id": "AGT-009", "seniority": "Junior", "hire_year": 2021},
    {"name": "Tyler Brown", "id": "AGT-010", "seniority": "Junior", "hire_year": 2022},
    {"name": "Jessica Lee", "id": "AGT-011", "seniority": "Junior", "hire_year": 2022},
    {"name": "Andrew Garcia", "id": "AGT-012", "seniority": "Junior", "hire_year": 2022},
]

SALES_CHANNELS = ["Direct", "Broker", "Online", "Referral"]
CHANNEL_WEIGHTS = [0.30, 0.35, 0.20, 0.15]

PAYMENT_FREQUENCIES = ["Monthly", "Quarterly", "Semi-Annual", "Annual"]
PAYMENT_FREQ_WEIGHTS = [0.45, 0.20, 0.15, 0.20]

CUSTOMER_SEGMENTS = ["Individual", "Family", "Small Business", "Corporate"]

AGE_BRACKETS = ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
AGE_WEIGHTS = [0.08, 0.22, 0.28, 0.24, 0.13, 0.05]

POLICY_STATUSES = ["Active", "Renewed", "Cancelled", "Lapsed", "Claims Pending"]

# ─── Seasonal Factors ────────────────────────────────────────────────────────

SEASONAL_FACTORS = {
    1: 0.85, 2: 0.88, 3: 1.02, 4: 1.05,
    5: 1.08, 6: 1.10, 7: 1.02, 8: 0.98,
    9: 0.95, 10: 1.00, 11: 0.97, 12: 0.90,
}

# Hurricane season bump for claims (Jun-Nov)
HURRICANE_CLAIM_FACTOR = {
    1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0,
    5: 1.05, 6: 1.15, 7: 1.25, 8: 1.40,
    9: 1.55, 10: 1.30, 11: 1.10, 12: 1.0,
}


def generate_transaction_date(year, month):
    """Generate a random date within the given year/month."""
    if month == 12:
        max_day = 31
    elif month in [4, 6, 9, 11]:
        max_day = 30
    elif month == 2:
        max_day = 29 if year % 4 == 0 else 28
    else:
        max_day = 31
    day = np.random.randint(1, max_day + 1)
    return datetime(year, month, day)


def generate_policy_number(idx, product_code):
    """Generate a realistic policy number."""
    prefix_map = {
        "Auto": "AUT", "Home": "HOM", "Life": "LIF",
        "Health": "HLT", "Commercial": "COM"
    }
    prefix = prefix_map[product_code]
    return f"KAT-{prefix}-{idx:06d}"


def calculate_commission(premium, channel, seniority):
    """Calculate agent commission based on channel and seniority."""
    base_rates = {
        "Direct": 0.10, "Broker": 0.15, "Online": 0.05, "Referral": 0.12
    }
    seniority_bonus = {
        "Senior": 0.03, "Mid": 0.015, "Junior": 0.0
    }
    rate = base_rates[channel] + seniority_bonus[seniority]
    return round(premium * rate, 2)


def determine_policy_status(product, tenure_months, has_claim, claim_amount, premium):
    """Determine policy status based on various factors."""
    if has_claim and claim_amount > premium * 2:
        if np.random.random() < 0.15:
            return "Cancelled"
    if tenure_months <= 12:
        churn_prob = 0.23  # 23% first-year churn
    elif tenure_months <= 24:
        churn_prob = 0.14
    else:
        churn_prob = 0.08  # 8% for 3+ year customers

    if np.random.random() < churn_prob * 0.3:
        return np.random.choice(["Cancelled", "Lapsed"], p=[0.6, 0.4])

    if has_claim:
        return "Claims Pending" if np.random.random() < 0.3 else "Active"

    if tenure_months >= 12:
        return "Renewed" if np.random.random() < 0.7 else "Active"

    return "Active"


def generate_data():
    """Generate the full dataset."""
    print("=" * 60)
    print("KAT Insurance Co. - Sales Data Generator")
    print("=" * 60)

    records = []
    idx = 0

    # Generate monthly transaction volumes
    months = []
    for year in [2022, 2023]:
        for month in range(1, 13):
            months.append((year, month))

    base_monthly = NUM_RECORDS // len(months)

    for year, month in months:
        # Seasonal volume adjustment
        seasonal = SEASONAL_FACTORS[month]
        # Slight growth in 2023
        yearly_growth = 1.0 if year == 2022 else 1.06
        month_volume = int(base_monthly * seasonal * yearly_growth)
        # Add some noise
        month_volume += np.random.randint(-50, 50)

        for _ in range(month_volume):
            idx += 1

            # Select product line
            products = list(PRODUCT_LINES.keys())
            weights = [PRODUCT_LINES[p]["weight"] for p in products]
            # Shift toward commercial in 2023
            if year == 2023:
                weights[4] *= 1.08  # Commercial boost
                weights[0] *= 0.97  # Auto slight decline
            total = sum(weights)
            weights = [w / total for w in weights]
            product = np.random.choice(products, p=weights)
            config = PRODUCT_LINES[product]

            # Select region
            regions = list(REGIONS.keys())
            reg_weights = [REGIONS[r]["weight"] for r in regions]
            region = np.random.choice(regions, p=reg_weights)
            region_info = REGIONS[region]
            state = np.random.choice(region_info["states"])

            # Generate premium
            base_premium = np.random.normal(config["premium_mean"], config["premium_std"])
            base_premium = np.clip(base_premium, config["premium_range"][0], config["premium_range"][1])
            # Regional adjustment
            base_premium *= region_info["performance_factor"]
            # 2023 growth
            if year == 2023:
                base_premium *= (1 + config["growth_rate_2023"])
            premium = round(base_premium, 2)

            # Deductible
            deductible = np.random.choice(config["deductible_options"])

            # Claims
            claim_prob = config["claim_probability"]
            # Hurricane season adjustment for Home and Auto
            if product in ["Home", "Auto"]:
                claim_prob *= HURRICANE_CLAIM_FACTOR[month]
                # Florida and Gulf Coast higher hurricane risk
                if region in ["Florida", "Gulf Coast"]:
                    claim_prob *= 1.2

            has_claim = np.random.random() < claim_prob
            if has_claim:
                claim_amount = max(0, np.random.normal(
                    config["claim_severity_mean"],
                    config["claim_severity_std"]
                ))
                claim_amount = round(claim_amount, 2)
                num_claims = np.random.choice([1, 2, 3], p=[0.75, 0.20, 0.05])
            else:
                claim_amount = 0.0
                num_claims = 0

            # Agent
            agent = np.random.choice(AGENTS)

            # Channel
            channel = np.random.choice(SALES_CHANNELS, p=CHANNEL_WEIGHTS)

            # Customer demographics
            age_bracket = np.random.choice(AGE_BRACKETS, p=AGE_WEIGHTS)
            gender = np.random.choice(["Male", "Female"], p=[0.48, 0.52])

            if product == "Commercial":
                segment = np.random.choice(
                    ["Small Business", "Corporate"], p=[0.65, 0.35]
                )
            elif product == "Health" and np.random.random() < 0.4:
                segment = "Family"
            else:
                segment = np.random.choice(
                    ["Individual", "Family"], p=[0.60, 0.40]
                )

            # Payment
            payment_freq = np.random.choice(PAYMENT_FREQUENCIES, p=PAYMENT_FREQ_WEIGHTS)

            # Tenure (months since original policy purchase)
            if year == 2022:
                tenure = np.random.randint(0, 36)
            else:
                tenure = np.random.randint(0, 48)
            is_new_business = tenure == 0

            # Commission
            commission = calculate_commission(premium, channel, agent["seniority"])

            # Admin/operating cost (rough allocation per policy)
            admin_cost = round(premium * np.random.uniform(0.08, 0.18), 2)

            # Policy status
            status = determine_policy_status(
                product, tenure, has_claim, claim_amount, premium
            )

            # Renewal discount
            if tenure >= 12:
                renewal_discount = round(np.random.choice([0, 0.03, 0.05, 0.08, 0.10],
                    p=[0.30, 0.25, 0.25, 0.12, 0.08]) * premium, 2)
            else:
                renewal_discount = 0.0

            # Net premium after discount
            net_premium = round(premium - renewal_discount, 2)

            # Loss ratio for this transaction
            loss_ratio = round(claim_amount / net_premium, 4) if net_premium > 0 else 0.0

            # Underwriting result
            underwriting_result = round(net_premium - claim_amount - commission - admin_cost, 2)

            # Transaction date
            txn_date = generate_transaction_date(year, month)

            # Policy number
            policy_number = generate_policy_number(idx, product)

            # Customer ID (some customers have multiple policies)
            customer_id = f"CUST-{np.random.randint(1, 35000):05d}"

            record = {
                "transaction_id": f"TXN-{idx:07d}",
                "transaction_date": txn_date.strftime("%Y-%m-%d"),
                "policy_number": policy_number,
                "customer_id": customer_id,
                "product_line": product,
                "region": region,
                "state": state,
                "agent_name": agent["name"],
                "agent_id": agent["id"],
                "agent_seniority": agent["seniority"],
                "sales_channel": channel,
                "customer_segment": segment,
                "customer_age_bracket": age_bracket,
                "customer_gender": gender,
                "gross_premium": premium,
                "renewal_discount": renewal_discount,
                "net_premium": net_premium,
                "deductible": deductible,
                "claim_amount": claim_amount,
                "num_claims": num_claims,
                "commission": commission,
                "admin_cost": admin_cost,
                "loss_ratio": loss_ratio,
                "underwriting_result": underwriting_result,
                "payment_frequency": payment_freq,
                "policy_tenure_months": tenure,
                "is_new_business": is_new_business,
                "policy_status": status,
            }
            records.append(record)

    df = pd.DataFrame(records)

    # Sort by date
    df = df.sort_values("transaction_date").reset_index(drop=True)

    # Save
    df.to_csv(OUTPUT_FILE, index=False)

    # Print summary
    print(f"\nGenerated {len(df):,} transaction records")
    print(f"Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE) / (1024*1024):.1f} MB")
    print(f"\n{'─' * 40}")
    print("Product Line Distribution:")
    for product, count in df["product_line"].value_counts().items():
        pct = count / len(df) * 100
        print(f"  {product:<12} {count:>6,}  ({pct:.1f}%)")
    print(f"\n{'─' * 40}")
    print("Region Distribution:")
    for region, count in df["region"].value_counts().items():
        pct = count / len(df) * 100
        print(f"  {region:<20} {count:>6,}  ({pct:.1f}%)")
    print(f"\n{'─' * 40}")
    print(f"Total Gross Premium:    ${df['gross_premium'].sum():>14,.2f}")
    print(f"Total Net Premium:      ${df['net_premium'].sum():>14,.2f}")
    print(f"Total Claims:           ${df['claim_amount'].sum():>14,.2f}")
    print(f"Overall Loss Ratio:     {df['claim_amount'].sum() / df['net_premium'].sum():.2%}")
    print(f"Total Commission:       ${df['commission'].sum():>14,.2f}")
    print(f"Total Admin Cost:       ${df['admin_cost'].sum():>14,.2f}")
    print("=" * 60)


if __name__ == "__main__":
    generate_data()
