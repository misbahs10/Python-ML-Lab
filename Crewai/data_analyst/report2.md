# Business Sales Report  

*Date range: 2026‑08‑01 to 2026‑08‑08*  

---

## Executive Summary  
- The one‑week snapshot shows **$42,000** in revenue from **64 units** sold.  
- **Phones** dominate performance, delivering **57 % of units** and **53 % of revenue**.  
- **Karachi** is the strongest market, contributing **44 % of units** and **41 % of revenue**.  
- **Tablets** generate the lowest return, representing **19 % of units** but only **11 % of revenue**.  
- A strong positive link (Pearson ≈ 0.83) exists between units sold and revenue, confirming that higher volume drives higher earnings.  
- Data quality is excellent – no missing, duplicate, or negative values.  

These insights suggest focusing resources on phones and the Karachi market, while reviewing the tablet offering.

---

## Dataset Overview  

| Attribute | Details |
|-----------|---------|
| **Rows** | 8 |
| **Columns** | 5 |
| **Column Names** | `Date`, `Product`, `Region`, `Units_Sold`, `Revenue` |
| **Date Range** | 2026‑08‑01 to 2026‑08‑08 (single week) |
| **Data Types** | Date (string), Product (string), Region (string), Units_Sold (integer), Revenue (integer) |

---

## Data Quality  

| Issue | Count |
|-------|-------|
| Missing values | 0 |
| Duplicate rows | 0 |
| Negative/zero `Units_Sold` | 0 |
| Negative/zero `Revenue` | 0 |

*Conclusion:* The dataset is clean; no preprocessing required.

---

## Key Findings  

1. **Product Performance**  
   - **Phone**: 37 units (57.8 % of total) → $22,200 revenue (52.9 %). Average revenue per unit: **$600**.  
   - **Laptop**: 15 units (23.4 %) → $15,000 revenue (35.7 %). Avg. revenue per unit: **$1,000**.  
   - **Tablet**: 12 units (18.8 %) → $4,800 revenue (11.4 %). Avg. revenue per unit: **$400**.  

2. **Regional Performance**  
   - **Karachi**: 28 units (43.8 %) → $17,200 revenue (40.9 %). Avg. revenue per unit: **$614**.  
   - **Lahore**: 19 units (29.7 %) → $14,200 revenue (33.8 %). Avg. revenue per unit: **$747**.  
   - **Islamabad**: 17 units (26.5 %) → $10,600 revenue (25.2 %). Avg. revenue per unit: **$624**.  

3. **Revenue‑Units Relationship**  
   - Pearson correlation = **0.83** (strong positive).  

4. **Outliers / Anomalies**  
   - Highest single‑day sale: 15 units (Phone, Karachi) → $9,000 revenue.  
   - Lowest sale: 3 units (Laptop, Islamabad) → $1,600 revenue.  
   - No extreme values beyond expected range.

---

## Important Trends and Patterns  

- **Phone dominance** across both volume and earnings.  
- **Karachi** outperforms other regions in absolute sales, making it the most valuable market.  
- **Laptop** earns higher revenue per unit ($1,000) despite lower volume, indicating a premium pricing strategy.  
- **Tablet** shows a low revenue per unit ($400) and a modest share of total revenue, suggesting weak demand or pricing issues.  

---

## Correlations and Anomalies  

- **Strong correlation (0.83)** between units sold and revenue confirms that boosting unit sales will proportionally increase revenue.  
- No data‑quality anomalies (e.g., missing or negative values) to distort analysis.  
- The variation in average revenue per unit across products points to differing price points, not data errors.

---

## Business Insights  

- **Prioritize phone inventory and marketing** to capture the bulk of sales.  
- **Invest in Karachi** with targeted promotions, stock allocation, and possibly localized campaigns, as it drives the largest share of revenue.  
- **Re‑evaluate tablet strategy**: low revenue contribution may be due to price, insufficient demand, or limited promotion. Consider pricing adjustments, bundling, or phased discontinuation.  
- **Leverage the laptop’s higher price point** by cross‑selling accessories or service packages to increase overall basket size.  
- **Short‑term focus:** The dataset reflects only one week; trends should be validated with longer‑term data before committing to major strategic shifts.

---

## Practical Recommendations  

1. **Inventory Management**  
   - Increase phone stock levels in Karachi and Lahore to avoid stock‑outs.  
   - Maintain sufficient laptop inventory to meet premium demand, especially in Lahore where average revenue per unit is highest.  

2. **Marketing Actions**  
   - Deploy phone‑focused advertising in Karachi (e.g., localized digital ads, radio spots).  
   - Run a limited‑time tablet promotion (discounts or bundles) to test price elasticity.  

3. **Pricing Review**  
   - Conduct a pricing analysis for tablets to identify if a higher price point is feasible without eroding demand.  
   - Explore premium accessory bundles for laptops to boost average transaction value.  

4. **Data Expansion**  
   - Collect sales data over multiple weeks/months to confirm seasonality and longer‑term trends.  
   - Track additional metrics (e.g., profit margin, customer acquisition cost) for deeper insight.  

5. **Performance Monitoring**  
   - Set weekly KPIs: total units, revenue by product, revenue by region, and average revenue per unit.  
   - Review KPI dashboards regularly to detect shifts early and adjust tactics.  

---

## Conclusion  

The week‑long sales snapshot reveals a clear hierarchy: **Phones** lead in both volume and revenue, with **Karachi** as the top regional market. **Laptops** contribute high revenue per unit, while **Tablets** lag significantly. The strong correlation between units sold and revenue underscores the importance of volume‑driven strategies.  

By concentrating inventory and marketing resources on phones and the Karachi market, while reassessing tablet positioning, the business can capitalize on existing strengths and address weak spots. Continued data collection will be essential to validate these findings over time and to refine strategic decisions