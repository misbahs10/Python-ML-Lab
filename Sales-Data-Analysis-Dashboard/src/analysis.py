"""
============================================
Sales Data Analysis Dashboard
Sales Analysis
============================================
"""

import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
from src.config import OUTPUT_DIR


def sales_analysis(data):

    print("\n" + "=" * 60)
    print(" SALES ANALYSIS ")
    print("=" * 60)

    # -----------------------------
    # Total Sales
    # -----------------------------
    total_sales = data["Sales"].sum()

    print(f"\nTotal Sales : ${total_sales:,.2f}")

    # -----------------------------
    # Total Profit
    # -----------------------------
    total_profit = data["Profit"].sum()

    print(f"Total Profit : ${total_profit:,.2f}")

    # -----------------------------
    # Total Orders
    # -----------------------------
    total_orders = data["Order ID"].nunique()

    print(f"Total Orders : {total_orders}")

    # -----------------------------
    # Total Customers
    # -----------------------------
    total_customers = data["Customer ID"].nunique()

    print(f"Total Customers : {total_customers}")

    # ===========================================================
    # Monthly Sales
    # ===========================================================

    monthly_sales = data.groupby("Month")["Sales"].sum()

    print("\nMonthly Sales\n")
    print(monthly_sales)

    plt.figure(figsize=(10,5))

    monthly_sales.plot(marker="o")

    plt.title("Monthly Sales")

    plt.xlabel("Month")

    plt.ylabel("Sales")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/monthly_sales.png")

    plt.show()

    # ===========================================================
    # Monthly Profit
    # ===========================================================

    monthly_profit = data.groupby("Month")["Profit"].sum()

    print("\nMonthly Profit\n")

    print(monthly_profit)

    plt.figure(figsize=(10,5))

    monthly_profit.plot(marker="o")

    plt.title("Monthly Profit")

    plt.xlabel("Month")

    plt.ylabel("Profit")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/monthly_profit.png")

    plt.show()

    # ===========================================================
    # Region Wise Sales
    # ===========================================================

    region_sales = data.groupby("Region")["Sales"].sum()

    print("\nRegion Wise Sales\n")

    print(region_sales)

    plt.figure(figsize=(8,5))

    region_sales.plot(kind="bar")

    plt.title("Region Wise Sales")

    plt.ylabel("Sales")

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/region_sales.png")

    plt.show()

    # ===========================================================
    # Category Wise Sales
    # ===========================================================

    category_sales = data.groupby("Category")["Sales"].sum()

    print("\nCategory Wise Sales\n")

    print(category_sales)

    plt.figure(figsize=(8,5))

    category_sales.plot(kind="bar")

    plt.title("Category Wise Sales")

    plt.ylabel("Sales")

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/category_sales.png")

    plt.show()

    # ===========================================================
    # Top 10 Products
    # ===========================================================

    top_products = (
        data.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\nTop 10 Products\n")

    print(top_products)

    plt.figure(figsize=(12,6))

    top_products.plot(kind="bar")

    plt.title("Top 10 Products")

    plt.ylabel("Sales")

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/top_products.png")

    plt.show()

    return {
        "Sales": total_sales,
        "Profit": total_profit
    }