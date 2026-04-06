# Insurance Analytics — KAT Model

I'm in Gamma Iota Sigma (insurance/risk management fraternity) at UGA and wanted to actually understand how insurers analyze risk, not just hear about it in meetings. This project uses a catastrophe loss dataset to explore how natural disasters affect insurance claims.

## What's in here

- `data/` — catastrophe event data (storm type, region, insured losses, fatalities)
- `analysis/` — Python scripts that clean the data, run breakdowns by peril type and region, and look at loss trends over time
- `visualizations/` — charts generated from the analysis (loss by region, year-over-year trends, peril breakdown)
- `reports/` — written summaries of findings
- `excel_templates/` — Excel versions for people who prefer spreadsheets

## What I learned

- How to clean and reshape messy real-world data with pandas
- Catastrophe modeling basics — how insurers bucket events by peril type (hurricane, tornado, wildfire, etc.)
- Data visualization in Python (matplotlib/seaborn) — making charts that actually communicate something
- The difference between insured losses and total economic losses (it's huge)

## Tech

Python, pandas, matplotlib, seaborn, Excel

## To run

```bash
pip install -r requirements.txt
```
Then run the scripts in `analysis/` in order.
