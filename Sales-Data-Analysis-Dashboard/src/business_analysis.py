"""
============================================
Sales Data Analysis Dashboard
Business Analysis
============================================
"""

import pandas as pd # type: ignore
import matplotlib.pyplot as plt 


def business_analysis(data):

    print("\n" + "=" * 60)
    print(" BUSINESS ANALYSIS ")
    print("=" * 60)

    # ==========================================
    # Top 10 Profitable Products
    # ==========================================

    top_profit_products = (
        data.groupby("Product Name")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\nTop 10 Profitable Products\n")
    print(top_profit_products)

    plt.figure(figsize=(12,6))

    top_profit_products.plot(kind="bar")

    plt.title("Top 10 Profitable Products")

    plt.xlabel("Product Name")

    plt.ylabel("Profit")

    plt.tight_layout()

    plt.savefig("outputs/top_profit_products.png")

    plt.show()

    # ==========================================
    # Top 10 Customers
    # ==========================================

    top_customers = (
        data.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\nTop Customers\n")
    print(top_customers)

    plt.figure(figsize=(12,6))

    top_customers.plot(kind="bar", color="green")

    plt.title("Top 10 Customers")

    plt.ylabel("Sales")

    plt.tight_layout()

    plt.savefig("outputs/top_customers.png")

    plt.show()

    # ==========================================
    # State Wise Sales
    # ==========================================

    state_sales = (
        data.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nState Wise Sales\n")
    print(state_sales.head(15))

    plt.figure(figsize=(14,6))

    state_sales.head(15).plot(kind="bar")

    plt.title("Top 15 States by Sales")

    plt.ylabel("Sales")

    plt.tight_layout()

    plt.savefig("outputs/state_sales.png")

    plt.show()

    # ==========================================
    # Category Summary
    # ==========================================

    category_summary = (
        data.groupby("Category")[["Sales", "Profit"]]
        .sum()
    )

    print("\nCategory Summary\n")

    print(category_summary)

    category_summary.to_csv(
        "outputs/category_summary.csv"
    )

    print("\nCategory Summary Saved Successfully.")

    # ==========================================
    # Region Summary
    # ==========================================

    region_summary = (
        data.groupby("Region")[["Sales", "Profit"]]
        .sum()
    )

    print("\nRegion Summary\n")

    print(region_summary)

    region_summary.to_csv(
        "outputs/region_summary.csv"
    )

    print("\nRegion Summary Saved Successfully.")

    print("\nBusiness Analysis Completed Successfully.")