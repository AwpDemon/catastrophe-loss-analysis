# Executive Summary - KAT Insurance Co. Data Analytics

**Prepared for:** KAT Insurance Co. Executive Leadership
**Analyst:** Ali Askari
**Date:** Spring 2024 | Atlanta, GA

---

## Engagement Overview

This analytics engagement examined 65,000+ insurance sales transactions spanning January 2022 through December 2023 across KAT Insurance Co.'s five core product lines and twelve Southeastern U.S. states. The analysis employed Excel PivotTables with calculated fields for multi-dimensional financial profiling, supplemented by Python-based statistical validation.

## Key Findings

### Five Financial Performance Trends Identified

**1. Premium Revenue Growth: Commercial Lines Leading**
- Total portfolio grew 8-10% YoY (2022 to 2023)
- Commercial insurance outpaced all other lines with 12%+ YoY growth
- Auto insurance showed early signs of market saturation (<5% growth)
- Recommendation: Accelerate commercial line expansion while defending auto market share through targeted pricing

**2. Loss Ratio Volatility: Hurricane Season Impact**
- Q3 (July-September) loss ratios spike approximately 15 percentage points above baseline
- Home and Auto lines in Florida and Gulf Coast drive the majority of seasonal claims
- Annual average loss ratio remains within acceptable range, but Q3 distorts quarterly reporting
- Recommendation: Implement dynamic reserve adjustments and catastrophe reinsurance review for Q3

**3. Regional Profitability Gaps: Metro vs. Rural**
- Atlanta Metro generates approximately 3x the premium volume of comparable rural regions
- However, underwriting profit ratio is only ~1.8x, indicating diminishing marginal returns
- Rural territories (Kentucky, Arkansas) show higher per-policy profitability
- Recommendation: Rebalance growth investment to capture underserved rural markets

**4. Product Mix: Favorable Shift Toward Commercial**
- Commercial lines gained approximately 8 percentage points in portfolio mix share
- Commercial underwriting margins exceed personal lines by 5-8 percentage points
- Health insurance cross-sell attachment rate remains below target at ~12%
- Recommendation: Invest in commercial distribution capabilities; launch health cross-sell campaign

**5. Customer Retention: Early Churn is the Critical Window**
- First-year policyholders churn at approximately 23%
- Churn rate declines to approximately 8% for customers with 3+ years tenure
- Renewal discount sensitivity analysis supports retention pricing in the 12-24 month window
- Recommendation: Implement tiered retention program targeting the 7-18 month "danger zone"

## Reporting Accuracy Improvement

The analysis identified and corrected five data definition and calculation inconsistencies that were causing approximately 20% variance in reported financial figures:

1. Gross vs. net premium inconsistency in departmental reports
2. Paid vs. incurred loss ratio basis mismatch
3. Commission accrual timing discrepancies
4. Administrative cost allocation methodology variance
5. Multi-policy customer double-counting in segment reports

All five issues have been documented and resolved in the standardized reporting framework.

## Financial Impact Summary

| Opportunity | Estimated Annual Impact |
|-------------|------------------------|
| Segment repricing | $250K - $500K |
| Channel mix optimization | $150K - $300K |
| Cross-sell program (Auto+Home) | $200K - $400K |
| Renewal discount rationalization | $100K - $200K |
| Agent productivity coaching | 10-15% premium lift |
| Admin cost reduction | $100K - $200K |
| **Total Estimated Impact** | **$800K - $1.6M** |

## Methodology

- **Primary Tool:** Microsoft Excel (PivotTables, calculated fields, conditional formatting)
- **Validation:** Python (pandas, matplotlib) for statistical cross-checks
- **Data Volume:** 65,000+ transactions, 28 fields, 24 months
- **Techniques:** Cross-tabulation, YoY variance analysis, loss ratio trending, cohort analysis, geographic profiling

## Next Steps

1. Actuarial validation of repricing recommendations (Q3 2024)
2. IT implementation of standardized reporting definitions (Q2 2024)
3. Launch Auto+Home cross-sell pilot in Atlanta Metro (Q3 2024)
4. Quarterly retention scorecard implementation (Q2 2024)
5. Agent performance coaching program rollout (Q3 2024)
