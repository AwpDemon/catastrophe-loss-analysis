# KAT Insurance — Portfolio Analytics

I worked through a dataset of 65,000+ insurance sales transactions (2022–2023, Southeastern US, 5 product lines) trying to answer the question I kept hearing at Gamma Iota Sigma events: *where is an insurer actually making or losing money, and why?* This is the analysis.

## Findings

**Q3 blows up the loss ratio, and it's geographic.** Loss ratios spike ~15 points above baseline in July–September every year. Decomposing the spike, ~40% comes from home claims in Florida and the Gulf Coast. Not a surprise (hurricanes) but the size of it was — it means annual-average reserve estimates systematically under-reserve Q3. Florida and Gulf Coast premiums probably aren't pricing in the catastrophe loading fully.

![Monthly loss ratio trend](visualizations/02_monthly_loss_ratio_trend.png)

**Commercial lines are the growth engine; auto is saturating.** YoY premium growth: Commercial ~12%, Health ~10%, Home ~8%, Life ~5%, Auto ~4%. Commercial also has wider underwriting margins than personal lines. The portfolio mix shift toward commercial improved margins structurally — not a one-time rate action.

![Premium YoY by line](visualizations/01_premium_yoy_comparison.png)

**Retention falls off a cliff in year one.** First-year churn was ~23%, dropping to ~8% for customers with 3+ years tenure. The 7–18 month window is where money walks out the door, and most retention discounts hit *after* that window. Repricing the renewal discount curve to front-load it is probably worth $100–200K annually.

## Methodology

Primary tool was Excel — PivotTables with calculated fields (loss ratio, combined ratio, YoY growth, retention rate), conditional formatting for the regional heatmaps. Python (pandas, matplotlib, seaborn) for cross-validation and the final chart set in `visualizations/`. Analysis scripts in `analysis/01…05.py` reproduce each pivot programmatically so the numbers can be re-run against new data.

Full writeup in [`reports/executive_summary.md`](reports/executive_summary.md). Per-trend detail in `reports/trend_1…trend_5.md`. Dataset schema in [`data/data_description.md`](data/data_description.md).

## Run

```bash
pip install -r requirements.txt
python data/generate_sales_data.py        # synthesizes the 65K-row dataset
python visualizations/generate_charts.py  # regenerates the 10 charts
```

Data is synthetic but calibrated to plausible industry ratios (43.6% overall loss ratio, ~22% admin + commission expense).
