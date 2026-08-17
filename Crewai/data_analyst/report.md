# Sales Data Analysis Report  

**Dataset:** `sales.csv` (E:/Machine-Learning-Projects/Python-ML-Lab/Crewai/data_analyst/)  
**Period Covered:** 1 Aug 2026 – 8 Aug 2026 (8 consecutive days)  

---  

## Executive Summary
- The dataset contains **8 daily sales records** for three product types (Laptop, Phone, Tablet) across three regions (Karachi, Lahore, Islamabad).  
- Data quality is excellent: **no missing values, no duplicates, and consistent formatting**.  
- **Phones generate the largest share of revenue (≈ 53 %)**, followed by Laptops and Tablets.  
- Each product has a **fixed unit price** (Laptop = 1 000, Phone = 600, Tablet = 400).  
- **Karachi shows the strongest single‑day revenue** (9 000) driven by a high‑volume Phone sale.  
- Units sold and revenue are strongly linked (Pearson ≈ 0.83).  

**Key business implication:** Prioritising Phone inventory and marketing, especially in Karachi, is likely to boost overall revenue.  

---  

## Dataset Overview  

| Attribute | Detail |
|-----------|--------|
| **Rows (records)** | 8 |
| **Columns** | 5 |
| **Column names** | `Date`, `Product`, `Region`, `Units_Sold`, `Revenue` |
| **Date range** | 2026‑08‑01 → 2026‑08‑08 (continuous) |
| **Products** | Laptop, Phone, Tablet |
| **Regions** | Karachi, Lahore, Islamabad |

### Data Types  

| Column | Detected Type |
|--------|---------------|
| Date | string (ISO‑date) – should be cast to **datetime** for time‑series work |
| Product | string (categorical) |
| Region | string (categorical) |
| Units_Sold | int64 |
| Revenue | int64 |

---  

## Data Quality  

| Issue | Count | Comment |
|-------|-------|---------|
| Missing values | 0 | All fields populated |
| Duplicate rows | 0 | Every record is unique |
| Inconsistent formatting | 0 | Text fields clean; numeric fields are whole numbers |
| Data‑type mismatch | 0 (except Date stored as string) | Convert `Date` to datetime for analysis |

**Conclusion:** The dataset is clean and ready for analysis after a simple date conversion.  

---  

## Key Findings  

1. **Revenue per unit is constant within each product**  
   - Laptop: **1 000** per unit  
   - Phone: **600** per unit  
   - Tablet: **400** per unit  

2. **Revenue contribution by product**  
   - Phone: **22 200** (≈ 53 % of total)  
   - Laptop: **15 000** (≈ 36 %)  
   - Tablet: **4 800** (≈ 12 %)  

3. **Regional performance**  
   - Karachi: 3 records, includes the highest single‑day revenue (9 000) from a Phone sale.  
   - Islamabad: 3 records, moderate sales.  
   - Lahore: 2 records, lower high‑value sales.  

4. **Daily sales variability** (units & revenue) is driven by the mix of products sold rather than overall demand spikes.  

5. **Strong correlation** between units sold and revenue (Pearson ≈ 0.83), reflecting the fixed pricing per product.  

---  

## Important Trends & Patterns  

| Trend | Observation | Business Meaning |
|-------|-------------|-----------------|
| **Product‑level pricing** | Fixed price per product, no discounts observed. | Pricing strategy is simple; any future price changes can be evaluated per product line. |
| **Phone dominance** | Phones generate the most revenue despite equal transaction count to Laptops. | High demand for Phones; scaling Phone inventory could raise total revenue. |
| **Regional hotspot** | Karachi’s single‑day revenue peaks at 9 000 (Phone, 15 units). | Karachi is a high‑potential market for Phones; targeted promotions may yield strong returns. |
| **Day‑to‑day fluctuation** | Daily units: 5, 12, 3, 8, 15, 7, 4, 10; Daily revenue: 5 000, 7 200, 3 000, 3 200, 9 000, 7 000, 1 600, 6 000. | Variability aligns with which product is sold each day; managing product mix can smooth revenue streams. |

---  

## Correlations and Anomalies  

- **Correlation (Units_Sold ↔ Revenue):** 0.83 (strong positive).  
  - Explanation: Revenue = Units_Sold × (product‑specific price).  

- **Anomalies / Outliers** (based on the small sample):  
  - **Units_Sold = 15 (Phone, Karachi)** – highest volume, but consistent with Phone’s popularity.  
  - **Revenue = 1 600 (Tablet, Islamabad)** – lowest revenue, reflecting Tablet’s lower unit price.  

No data quality issues (missing/duplicate) were detected.  

---  

## Business Insights  

1. **Focus on Phones to maximise revenue** – Phones already deliver the largest share; increasing stock levels, expanding marketing, or bundling accessories could further lift sales.  

2. **Leverage Karachi’s strong Phone demand** – Consider region‑specific campaigns (e.g., flash sales, localized advertising) to capture more of the market’s appetite.  

3. **Maintain simple pricing** – Since each product has a fixed price, any discount strategy should be evaluated carefully to avoid eroding the clear price‑product relationship.  

4. **Manage product mix for smoother daily revenue** – Ensure a balanced supply of high‑margin Phones while still offering Laptops and Tablets to meet diverse customer preferences.  

5. **Data readiness for advanced analytics** – With clean data, the next steps (forecasting, profit analysis) can be built quickly after converting the `Date` column to a proper datetime format.  

---  

## Practical Recommendations  

| Recommendation | Rationale | Suggested Action |
|----------------|----------|-------------------|
| **Convert `Date` to datetime** | Enables time‑series features (day‑of‑week, trends). | Update data pipeline; add a `Date` column of type datetime. |
| **Extend the data collection period** | Current 8‑day window is too short to confirm long‑term patterns. | Gather at least 3‑6 months of sales data. |
| **Add cost information** | Revenue alone does not reveal profitability. | Capture product cost per unit to compute margins. |
| **Segment analysis by Product × Region** | Identify region‑specific product strengths. | Create a pivot table showing units and revenue per product per region. |
| **Forecast unit sales** | Strong link between units and revenue; accurate forecasts drive inventory planning. | Apply simple time‑series models (e.g., ARIMA) after date conversion. |
| **Test promotional pricing** | Fixed pricing limits revenue growth opportunities. | Run A/B tests with limited‑time discounts on Phones in Karachi and measure impact on units and revenue. |
| **Monitor inventory levels** | High‑volume Phone sales could lead to stockouts. | Implement inventory alerts when projected demand exceeds current stock. |

---  

## Conclusion  

The sales dataset, though small, provides clear evidence that **Phones are the primary revenue driver**, especially in **Karachi**. Pricing is straightforward, with each product carrying a fixed unit price, making revenue directly proportional to units sold. Data quality is high, allowing immediate analytical work after a minor date‑type conversion.  

To capitalize on these insights, the business should **prioritise Phone inventory and targeted regional marketing**, while **expanding the dataset** and **adding cost data** to deepen profitability analysis. Implementing the recommended next steps will enable more robust forecasting, better inventory control, and data‑driven decision‑making for sustained revenue growth.  