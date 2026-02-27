# Trend 1: Premium Revenue Growth Patterns by Product Line

## Summary

Analysis of 65,000+ transactions reveals divergent premium growth trajectories across KAT Insurance Co.'s five product lines. Commercial insurance leads with approximately 12% YoY growth, while auto insurance shows early saturation signals at under 5% growth. The overall portfolio grew 8-10% from 2022 to 2023, driven primarily by commercial and health line expansion.

## Methodology

**Excel PivotTable Configuration:**
- **Rows:** Product Line
- **Columns:** Year (2022, 2023)
- **Values:** Sum of Net Premium
- **Calculated Field:** YoY Growth % = (2023 Value - 2022 Value) / 2022 Value

Additional pivot with quarterly granularity (Rows: Year-Quarter, Columns: Product Line) to identify intra-year trajectory patterns.

## Findings

### Annual Growth by Product Line

| Product Line | 2022 Premium | 2023 Premium | YoY Growth |
|-------------|-------------|-------------|-----------|
| Commercial | Baseline | ~+12% | Fastest growing |
| Health | Baseline | ~+10% | Rate increases + expansion |
| Home | Baseline | ~+8% | Steady, market-driven |
| Life | Baseline | ~+5% | Moderate, stable |
| Auto | Baseline | ~+4% | Near saturation |

### Key Observations

1. **Commercial Acceleration:** Commercial lines experienced the strongest growth, driven by small business segment expansion and favorable rate environment. This product line commands higher average premiums and wider underwriting margins.

2. **Auto Plateau:** Auto insurance growth has decelerated to near-GDP levels, suggesting market saturation in KAT's primary territories. Competitive pressure from digital-first insurers is compressing margins.

3. **Health Premium Inflation:** Health line growth is partially driven by medical cost inflation passed through in premium rates, not purely organic volume growth. Adjusting for rate increases, organic unit growth is approximately 4-5%.

4. **Quarterly Seasonality:** All lines show seasonal patterns—Q2 and Q3 are peak production quarters (spring/summer), while Q1 and Q4 lag. This pattern is consistent across both years.

5. **Portfolio Diversification:** The shift toward commercial lines is improving overall portfolio diversification and reducing dependence on high-frequency, low-severity personal lines.

## Implications

- Commercial line growth should be supported with additional distribution capacity and underwriting expertise
- Auto line strategy should pivot from growth to profitability optimization (tighter underwriting, pricing discipline)
- Health line growth masks underlying medical cost inflation that needs monitoring
- The favorable portfolio mix shift toward commercial is a positive structural trend for profitability

## Visualization Reference

- Chart: `01_premium_yoy_comparison.png` - Grouped bar chart comparing 2022 vs 2023 premium by product line
- Chart: `08_quarterly_premium_trend.png` - Line chart showing quarterly trajectory by product
