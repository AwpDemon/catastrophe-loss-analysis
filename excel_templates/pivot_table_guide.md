# Excel PivotTable Configuration Guide

## Overview

This document provides step-by-step instructions for recreating the 13 PivotTable analyses used in the KAT Insurance Co. data analytics project. Each PivotTable is configured with specific row/column fields, value aggregations, calculated fields, and formatting rules.

## Prerequisites

1. Open `data/kat_insurance_sales.csv` in Excel
2. Select all data (Ctrl+A) and format as Table (Ctrl+T)
3. Name the table "SalesData" (Table Design > Table Name)
4. Add helper columns as documented in `reports/methodology.md`

## PivotTable Setup Instructions

### PT1: Product Line Performance Summary

**Create:**
1. Insert > PivotTable > From Table "SalesData"
2. Place in new sheet named "PT_Product"

**Configure:**
```
Row Labels:     product_line
Values:
  - Count of transaction_id    → Rename: "Policy Count"
  - Sum of net_premium         → Rename: "Net Premium"  → Format: $#,##0
  - Sum of claim_amount        → Rename: "Claims"       → Format: $#,##0
  - Sum of commission          → Rename: "Commission"   → Format: $#,##0
  - Sum of admin_cost          → Rename: "Admin Cost"   → Format: $#,##0
  - Sum of underwriting_result → Rename: "UW Result"    → Format: $#,##0
```

**Add Calculated Fields** (PivotTable Analyze > Fields, Items & Sets > Calculated Field):
```
Name: Loss_Ratio
Formula: = claim_amount / net_premium
Format: 0.0%

Name: Expense_Ratio
Formula: = (commission + admin_cost) / net_premium
Format: 0.0%

Name: Combined_Ratio
Formula: = (claim_amount + commission + admin_cost) / net_premium
Format: 0.0%

Name: UW_Margin
Formula: = (net_premium - claim_amount - commission - admin_cost) / net_premium
Format: 0.0%
```

**Sort:** Right-click Net Premium column > Sort Largest to Smallest

**Conditional Formatting:**
- Select Loss_Ratio column > Home > Conditional Formatting > Color Scales > Green-Yellow-Red
- Select UW_Margin column > Conditional Formatting > Highlight Cell Rules > Less Than 0 > Red Fill

---

### PT2: Product Line x Year Comparison

**Configure:**
```
Row Labels:     product_line
Column Labels:  Year (helper column)
Values:         Sum of net_premium → Format: $#,##0
```

**Add Calculated Field:**
```
Name: YoY_Growth
Formula: Not directly possible as calculated field (cross-year).
Workaround: Add formulas outside the PivotTable:
  Cell: =([2023 Value]-[2022 Value])/[2022 Value]
  Format: +0.0%;-0.0%
```

**Conditional Formatting:**
- Data Bars on premium values (blue gradient)
- Icon Set (3 arrows) on YoY Growth column

---

### PT3: Regional Performance

**Configure:**
```
Row Labels:     region
Values:         Same as PT1 (all financial metrics + calculated fields)
Sort:           Net Premium descending
```

**Conditional Formatting:**
- Color scale on UW_Margin: Red (#FF0000) for values < 0%, Green (#00B050) for values > 10%
- Bold formatting on Grand Total row

---

### PT4: Region x Product Matrix

**Configure:**
```
Row Labels:     region
Column Labels:  product_line
Values:         Sum of net_premium → Format: $#,##0
Grand Totals:   Show for Rows and Columns
```

**Conditional Formatting:**
- Select all data cells (excluding totals)
- Color Scales > Green-White-Red (Green = highest premium)

---

### PT5: Sales Channel Analysis

**Configure:**
```
Row Labels:     sales_channel
Values:         All financial metrics + calculated fields
Additional:
  Name: Commission_Rate
  Formula: = commission / net_premium
  Format: 0.0%
```

---

### PT6: Quarterly Trends

**Configure:**
```
Row Labels:     Year-Quarter (helper column)
Values:
  - Count of transaction_id
  - Sum of net_premium
  - Sum of claim_amount
  - Loss_Ratio (calculated field)
```

**Insert Chart:**
1. Select PivotTable
2. PivotTable Analyze > PivotChart
3. Chart Type: Combo (Column for Premium, Line for Loss Ratio)
4. Loss Ratio on Secondary Axis
5. Format: Premium bars in blue, Loss Ratio line in red with markers

---

### PT7: Agent Seniority x Product

**Configure:**
```
Row Labels:     agent_seniority
Column Labels:  product_line
Values:         Sum of net_premium, Sum of commission
Report Filter:  Year
```

---

### PT8: Customer Segment Performance

**Configure:**
```
Row Labels:     customer_segment
Values:         All financial metrics + calculated fields
Slicers:        product_line, Year (Insert Slicer from PivotTable Analyze)
```

---

### PT9: Age Bracket x Product

**Configure:**
```
Row Labels:     customer_age_bracket
Column Labels:  product_line
Values:         Sum of net_premium, Count of transaction_id
```

**Note:** Age brackets should be in natural order. If they sort alphabetically, use a custom sort list:
Right-click > Sort > More Sort Options > Manual (drag to reorder)

---

### PT10: Policy Status Breakdown

**Configure:**
```
Row Labels:     product_line
Column Labels:  policy_status
Values:         Count of transaction_id
```

**Add formula outside PivotTable:**
```
Churn_Rate = (Cancelled + Lapsed) / Row Total
Format: 0.0%
```

---

### PT11: Payment Frequency x Channel

**Configure:**
```
Row Labels:     payment_frequency
Column Labels:  sales_channel
Values:         Sum of net_premium, Average of net_premium
Grand Totals:   Rows and Columns
```

---

### PT12: Agent Performance Ranking

**Configure:**
```
Row Labels:     agent_name (outer), agent_seniority (inner)
Values:
  - Count of transaction_id
  - Sum of net_premium
  - Sum of claim_amount
  - Loss_Ratio (calculated)
  - Sum of underwriting_result
Sort:           Net Premium descending
```

**Conditional Formatting:**
- Top 3 rules on Net Premium: Green fill
- Bottom 3 rules on Net Premium: Red fill

---

### PT13: Loss Ratio Heatmap

**Configure:**
```
Row Labels:     region
Column Labels:  Year-Quarter (helper column)
Values:         Loss_Ratio (calculated field)
Format:         0.0%
```

**Conditional Formatting:**
- Three-Color Scale:
  - Minimum (Green): Type=Number, Value=0.3
  - Midpoint (Yellow): Type=Number, Value=0.5
  - Maximum (Red): Type=Number, Value=0.8

---

## Slicer Configuration

### Create Slicers
1. Click any PivotTable
2. PivotTable Analyze > Insert Slicer
3. Check: product_line, Year, region, sales_channel
4. Click OK

### Connect Slicers to Multiple PivotTables
1. Right-click slicer > Report Connections
2. Check all PivotTables that should be filtered by that slicer

### Slicer Formatting
1. Slicer tab > Slicer Styles
2. Set columns = 5 (for product line), columns = 2 (for year)
3. Size: Width 200px, Height 120px per slicer

---

## Dashboard Assembly

### Sheet Setup
1. Create new sheet "Dashboard"
2. Set zoom to 85%
3. Hide gridlines (View > uncheck Gridlines)
4. Set print area to fit 1 page wide

### KPI Tiles (Row 1-3)
Create formatted cells with these formulas:
```
Total Premium:     =GETPIVOTDATA("net_premium",PT_Product!$A$3)
Total Claims:      =GETPIVOTDATA("claim_amount",PT_Product!$A$3)
Portfolio LR:      =GETPIVOTDATA("Loss_Ratio",PT_Product!$A$3)
Combined Ratio:    =GETPIVOTDATA("Combined_Ratio",PT_Product!$A$3)
UW Margin:         =GETPIVOTDATA("UW_Margin",PT_Product!$A$3)
```

### Charts
- Copy PivotCharts from individual sheets
- Paste as linked pictures (Paste Special > Linked Picture)
- Charts update automatically when PivotTables refresh

---

## Tips for Maintaining This Workbook

1. **Refresh Data:** Data tab > Refresh All (or Ctrl+Alt+F5)
2. **Add New Data:** Append rows to the SalesData table; PivotTables will include new rows on refresh
3. **Modify Calculated Fields:** PivotTable Analyze > Fields, Items & Sets > Calculated Field > select and edit
4. **Export to PDF:** File > Export > Create PDF, with "Active Sheets" or "Entire Workbook" selected
5. **Protect Structure:** Review > Protect Workbook (to prevent accidental sheet deletion)
