# KAT Insurance Co. - Dataset Description

## Overview

The dataset contains 65,000+ insurance sales transactions recorded by KAT Insurance Co. across the Southeastern United States from January 2022 through December 2023. Each row represents a single policy transaction, including new business, renewals, and claims activity.

## File

- **Filename:** `kat_insurance_sales.csv`
- **Records:** ~67,500
- **Fields:** 28 columns
- **Encoding:** UTF-8
- **Delimiter:** Comma

## Field Definitions

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | `transaction_id` | String | Unique transaction identifier (TXN-0000001) |
| 2 | `transaction_date` | Date | Transaction date (YYYY-MM-DD) |
| 3 | `policy_number` | String | Policy identifier (KAT-{PRODUCT}-000001) |
| 4 | `customer_id` | String | Customer identifier (CUST-00001) |
| 5 | `product_line` | String | Insurance product: Auto, Home, Life, Health, Commercial |
| 6 | `region` | String | Business region (8 regions) |
| 7 | `state` | String | U.S. state abbreviation |
| 8 | `agent_name` | String | Selling/servicing agent name |
| 9 | `agent_id` | String | Agent identifier (AGT-001) |
| 10 | `agent_seniority` | String | Agent level: Senior, Mid, Junior |
| 11 | `sales_channel` | String | Channel: Direct, Broker, Online, Referral |
| 12 | `customer_segment` | String | Individual, Family, Small Business, Corporate |
| 13 | `customer_age_bracket` | String | Age group: 18-25, 26-35, 36-45, 46-55, 56-65, 65+ |
| 14 | `customer_gender` | String | Male, Female |
| 15 | `gross_premium` | Float | Gross annual premium in USD |
| 16 | `renewal_discount` | Float | Discount applied for policy renewal |
| 17 | `net_premium` | Float | Premium after discount (gross - renewal discount) |
| 18 | `deductible` | Integer | Policy deductible amount in USD |
| 19 | `claim_amount` | Float | Total claims paid in USD (0 if no claim) |
| 20 | `num_claims` | Integer | Number of claims filed |
| 21 | `commission` | Float | Agent/broker commission in USD |
| 22 | `admin_cost` | Float | Allocated administrative/operating cost |
| 23 | `loss_ratio` | Float | Claim amount / Net premium (per-transaction) |
| 24 | `underwriting_result` | Float | Net premium - claims - commission - admin cost |
| 25 | `payment_frequency` | String | Monthly, Quarterly, Semi-Annual, Annual |
| 26 | `policy_tenure_months` | Integer | Months since original policy inception |
| 27 | `is_new_business` | Boolean | True if tenure = 0 (new policy) |
| 28 | `policy_status` | String | Active, Renewed, Cancelled, Lapsed, Claims Pending |

## Product Lines

| Product | Description | Approx. Share |
|---------|-------------|---------------|
| Auto | Personal automobile insurance | 32% |
| Home | Homeowners/property insurance | 26% |
| Life | Term and whole life insurance | 14% |
| Health | Individual and family health plans | 16% |
| Commercial | Business liability and property | 12% |

## Regions

| Region | States | Approx. Share |
|--------|--------|---------------|
| Atlanta Metro | GA | 22% |
| Florida | FL | 18% |
| Carolinas | NC, SC | 14% |
| Tennessee Valley | TN, AL | 12% |
| Gulf Coast | MS, LA | 10% |
| Virginia | VA | 10% |
| Kentucky | KY | 7% |
| Arkansas | AR | 7% |

## Calculated Fields (Used in Excel Analysis)

The following calculated fields were added in Excel PivotTables:

1. **Loss Ratio** = `claim_amount / net_premium`
2. **Expense Ratio** = `(commission + admin_cost) / net_premium`
3. **Combined Ratio** = `Loss Ratio + Expense Ratio`
4. **Underwriting Margin** = `1 - Combined Ratio`
5. **Revenue per Policy** = `net_premium` (aggregated via PivotTable)
6. **Claims Frequency** = `Count of claims / Count of policies` (per segment)
7. **Average Claim Severity** = `Sum of claim_amount / Count of claims` (where claims > 0)
8. **Retention Rate** = `Count of Renewed / (Count of Active + Renewed + Cancelled + Lapsed)`
9. **YoY Growth %** = `(Current Year Value - Prior Year Value) / Prior Year Value`
10. **Profit per Customer** = `Sum of underwriting_result / Count of unique customer_id`

## Data Quality Notes

- All premium values are annualized
- Claims amounts are cumulative for the transaction period
- Loss ratios > 1.0 indicate unprofitable transactions
- Some customers appear multiple times (multi-policy holders)
- Tenure of 0 months indicates new business written in that period
- Life insurance deductibles are set to $0 (not applicable)
