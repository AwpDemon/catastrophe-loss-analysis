# Trend 3: Regional Performance Disparities

## Summary

Analysis of premium volume and underwriting profitability across KAT Insurance Co.'s eight operating regions reveals significant performance gaps. Atlanta Metro generates approximately 3x the premium volume of comparable rural regions but only approximately 1.8x the underwriting profit, indicating diminishing marginal returns in saturated metro markets. Rural territories, while smaller in absolute volume, demonstrate higher per-policy profitability and represent untapped growth opportunities.

## Methodology

**Excel PivotTable Configuration:**

Pivot 1 - Regional Overview:
- **Rows:** Region
- **Values:** Count of Policies, Sum of Net Premium, Sum of Claims, Sum of Commission, Sum of Admin Cost, Sum of UW Result
- **Calculated Fields:** Loss Ratio, Expense Ratio, Combined Ratio, UW Margin, Premium per Policy, Profit per Policy

Pivot 2 - Region x Product Matrix:
- **Rows:** Region
- **Columns:** Product Line
- **Values:** Sum of Net Premium
- **Conditional Formatting:** Color scale (green = high, red = low)

Pivot 3 - Region x Quarter Loss Ratio:
- **Rows:** Region
- **Columns:** Year-Quarter
- **Values:** Calculated Loss Ratio
- **Conditional Formatting:** Three-color scale for loss ratio values

## Findings

### Regional Performance Scorecard

Regions ranked by total net premium volume:

1. **Atlanta Metro (GA)** - Highest volume, moderate profitability. Strong across all product lines. Benefits from large corporate customer base driving commercial premiums.

2. **Florida (FL)** - Second-highest volume but highest loss ratio due to hurricane exposure. Home insurance profitability is problematic; auto and commercial perform better.

3. **Carolinas (NC, SC)** - Balanced portfolio with moderate loss ratios. Consistent performer across quarters without extreme seasonal swings.

4. **Tennessee Valley (TN, AL)** - Mid-tier volume with above-average profitability. Lower competitive intensity provides pricing power.

5. **Gulf Coast (MS, LA)** - Weather-exposed similar to Florida but smaller scale. Loss ratio is elevated; profitability lags.

6. **Virginia (VA)** - Moderate volume, strong underwriting discipline. Highest average premium per policy in the portfolio.

7. **Kentucky (KY)** - Smaller market but strong per-policy profitability. Represents expansion opportunity.

8. **Arkansas (AR)** - Smallest region. Low volume but competitive cost structure yields favorable margins.

### Metro vs. Rural Economics

| Metric | Atlanta Metro | Rural Average (KY+AR+Gulf) |
|--------|--------------|---------------------------|
| Premium Volume | ~22% of portfolio | ~24% combined |
| Premium per Policy | Higher | Lower |
| Loss Ratio | Moderate | Lower |
| Expense Ratio | Higher | Lower |
| Profit per Policy | Moderate | Higher |
| Competitive Intensity | High | Low-Moderate |

Key insight: Atlanta Metro's higher expense structure (office costs, agent compensation, marketing) offsets its volume advantage. Rural regions benefit from lower cost bases and less competitive pressure on pricing.

### Product Line Performance by Region

- **Commercial:** Atlanta Metro dominates (~35% of all commercial premium). Corporate headquarters presence drives this concentration.
- **Auto:** Relatively evenly distributed, tracking population density.
- **Home:** Florida and Gulf Coast have the highest home premium but also the worst loss ratios (hurricane exposure).
- **Health:** Concentrated in metro areas (Atlanta, Florida, Carolinas) where employer-sponsored plans are more common.
- **Life:** Most evenly distributed across regions; least variation in profitability.

## Implications

1. **Growth Investment Rebalancing:** Shift incremental marketing and distribution investment toward high-margin rural territories (KY, AR, TN) that are currently under-penetrated.

2. **Florida Portfolio Review:** The Florida home insurance book requires actuarial review. Consider tighter underwriting criteria, higher deductible minimums, or selective non-renewal of highest-risk ZIP codes.

3. **Agent Deployment:** Agent recruitment and office expansion should prioritize mid-tier markets (Virginia, Tennessee Valley) where the profit-to-volume ratio is most favorable.

4. **Regional Expense Benchmarking:** Implement regional expense benchmarks using the lower-cost territories as the standard, with adjustment factors for cost-of-living differences.

## Visualization Reference

- Chart: `03_regional_performance_heatmap.png` - Region x Product underwriting result heatmap
- Chart: `07_channel_performance.png` - Channel performance metrics (regional overlay available in Excel)
