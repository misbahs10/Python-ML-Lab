"""
============================================
Sales Data Analysis Dashboard
Advanced Business Analysis
============================================
"""

import matplotlib.pyplot as plt
import pandas as pd # type: ignore


def advanced_analysis(data):

    print("\n" + "=" * 60)
    print("ADVANCED BUSINESS ANALYSIS")
    print("=" * 60)

    # ==========================================
    # Correlation Matrix
    # ==========================================

    correlation = data[["Sales", "Quantity", "Discount", "Profit"]].corr()

    print("\nCorrelation Matrix\n")
    print(correlation)

    plt.figure(figsize=(6,5))

    plt.imshow(correlation, cmap="coolwarm")

    plt.colorbar()

    plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45)

    plt.yticks(range(len(correlation.columns)), correlation.columns)

    plt.title("Correlation Matrix")

    plt.tight_layout()

    plt.savefig("outputs/correlation_heatmap.png")

    plt.show()

    # ==========================================
    # Discount vs Profit
    # ==========================================

    plt.figure(figsize=(8,5))

    plt.scatter(
        data["Discount"],
        data["Profit"]
    )

    plt.xlabel("Discount")

    plt.ylabel("Profit")

    plt.title("Discount vs Profit")

    plt.tight_layout()

    plt.savefig("outputs/discount_vs_profit.png")

    plt.show()

    # ==========================================
    # Year Wise Sales
    # ==========================================

    yearly_sales = data.groupby("Year")["Sales"].sum()

    print("\nYear Wise Sales\n")

    print(yearly_sales)

    plt.figure(figsize=(8,5))

    yearly_sales.plot(marker="o")

    plt.title("Year Wise Sales")

    plt.ylabel("Sales")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("outputs/yearly_sales.png")

    plt.show()

    # ==========================================
    # Segment Wise Sales
    # ==========================================

    segment_sales = data.groupby("Segment")["Sales"].sum()

    print("\nSegment Wise Sales\n")

    print(segment_sales)

    plt.figure(figsize=(8,5))

    segment_sales.plot(kind="bar")

    plt.title("Segment Wise Sales")

    plt.ylabel("Sales")

    plt.tight_layout()

    plt.savefig("outputs/segment_sales.png")

    plt.show()

    # ==========================================
    # Executive Summary
    # ==========================================

    summary = {
        "Total Sales": data["Sales"].sum(),
        "Total Profit": data["Profit"].sum(),
        "Average Sales": data["Sales"].mean(),
        "Average Profit": data["Profit"].mean(),
        "Total Customers": data["Customer ID"].nunique(),
        "Total Orders": data["Order ID"].nunique()
    }

    summary_df = pd.DataFrame(summary.items(), columns=["Metric", "Value"])

    print("\nExecutive Summary\n")

    print(summary_df)

    summary_df.to_csv(
        "outputs/executive_summary.csv",
        index=False
    )

    print("\nExecutive Summary Saved Successfully.")

    print("\nAdvanced Analysis Completed Successfully.")