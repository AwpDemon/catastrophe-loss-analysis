# KAT Insurance Co. - Data Analytics Project

**Location:** Atlanta, GA | **Period:** Spring 2024

## Overview

Comprehensive data analytics engagement with KAT Insurance Co., a mid-market property and casualty insurance carrier operating across the Southeastern United States. The project involved analyzing 65,000+ sales transactions spanning January 2022 through December 2023 to identify financial performance trends, optimize revenue streams, and improve cost efficiency across the organization's five core product lines.

## Objectives

- Profile and clean two years of transactional sales data (65,000+ records)
- Build dynamic Excel PivotTables with calculated fields for multi-dimensional analysis
- Identify key financial performance trends impacting profitability
- Deliver actionable recommendations for revenue optimization and cost reduction
- Improve reporting accuracy by standardizing data definitions and calculation methodology

## Key Results

| Metric | Outcome |
|--------|---------|
| Transactions Analyzed | 65,000+ |
| Financial Trends Identified | 5 major patterns |
| Reporting Accuracy Improvement | ~20% reduction in discrepancies |
| Product Lines Covered | Auto, Home, Life, Health, Commercial |
| Geographic Coverage | 12 Southeastern U.S. states |
| Analysis Period | Jan 2022 - Dec 2023 |

## Five Key Financial Performance Trends

1. **Premium Revenue Growth Patterns** - Identified divergent growth trajectories across product lines, with commercial insurance outpacing personal lines by 12% YoY while auto premiums showed signs of market saturation.

2. **Claims-to-Premium Ratio (Loss Ratio) Trends** - Discovered seasonal loss ratio spikes in Q3 (hurricane season) driving a 15-point swing in combined ratios, leading to recommendations for dynamic reserve adjustments.

3. **Regional Performance Disparities** - Mapped significant profitability gaps between metro and rural territories, with Atlanta metro generating 3x the premium volume but only 1.8x the underwriting profit of comparable rural regions.

4. **Product Mix Shifts and Profitability** - Tracked a portfolio shift toward higher-margin commercial lines (+8% mix share) while health insurance cross-sell rates remained below target at 12% attachment.

5. **Customer Retention and Churn Patterns** - Quantified a 23% first-year churn rate declining to 8% for 3+ year policyholders, with renewal discount sensitivity analysis informing a revised retention pricing strategy.

## Tools & Methodology

- **Primary Analysis:** Microsoft Excel (PivotTables, calculated fields, conditional formatting, data validation)
- **Supplementary Analysis:** Python (pandas, matplotlib, seaborn) for statistical validation and visualization
- **Data Volume:** 65,000+ transaction records, 28 fields per record
- **Techniques:** Pivot table cross-tabulation, YoY variance analysis, loss ratio trending, cohort analysis, geographic heat mapping

## Project Structure

```
kat-insurance-analytics/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── data/
│   ├── generate_sales_data.py         # Synthetic data generator (mirrors production schema)
│   └── data_description.md            # Dataset field documentation
├── analysis/
│   ├── 01_data_overview.py            # Data profiling and quality assessment
│   ├── 02_pivot_analysis.py           # PivotTable-equivalent analysis in pandas
│   ├── 03_financial_trends.py         # Five key financial trend analyses
│   ├── 04_revenue_optimization.py     # Revenue optimization insights
│   └── 05_cost_efficiency.py          # Cost efficiency analysis
├── visualizations/
│   ├── generate_charts.py             # Chart generation pipeline
│   └── .gitkeep
├── reports/
│   ├── executive_summary.md           # C-suite findings summary
│   ├── trend_1_premium_growth.md      # Premium growth deep-dive
│   ├── trend_2_claims_ratio.md        # Loss ratio analysis
│   ├── trend_3_regional_performance.md# Regional breakdown
│   ├── trend_4_product_mix.md         # Product mix analysis
│   ├── trend_5_customer_retention.md  # Retention/churn analysis
│   └── methodology.md                 # Excel methodology documentation
└── excel_templates/
    └── pivot_table_guide.md           # PivotTable configuration reference
```

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Generate the dataset
python data/generate_sales_data.py

# Run analyses (in order)
python analysis/01_data_overview.py
python analysis/02_pivot_analysis.py
python analysis/03_financial_trends.py
python analysis/04_revenue_optimization.py
python analysis/05_cost_efficiency.py

# Generate all visualizations
python visualizations/generate_charts.py
```

## Data Note

The dataset included in this repository is synthetically generated to mirror the schema, distributions, and statistical properties of the original KAT Insurance Co. transactional data. All personally identifiable information has been removed, and agent/broker names are fictitious. The analytical findings and trend patterns are preserved from the original engagement.

## Contact

Ali Askari - [GitHub](https://github.com/AwpDemon)
