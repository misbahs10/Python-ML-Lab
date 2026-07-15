"""
============================================
Sales Data Analysis Dashboard
Dashboard Charts
============================================
"""

import matplotlib.pyplot as plt


def create_dashboard(data):

    print("\nCreating Dashboard Charts...")

    # ======================================
    # Category Wise Sales (Pie Chart)
    # ======================================

    category_sales = data.groupby("Category")["Sales"].sum()

    plt.figure(figsize=(7,7))

    plt.pie(
        category_sales,
        labels=category_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Category Wise Sales")

    plt.savefig("outputs/category_pie_chart.png")

    plt.show()

    # ======================================
    # Region Wise Sales (Donut Chart)
    # ======================================

    region_sales = data.groupby("Region")["Sales"].sum()

    plt.figure(figsize=(7,7))

    plt.pie(
        region_sales,
        labels=region_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )

    centre_circle = plt.Circle((0,0),0.70,fc="white")

    fig = plt.gcf()

    fig.gca().add_artist(centre_circle)

    plt.title("Region Wise Sales")

    plt.savefig("outputs/region_donut_chart.png")

    plt.show()

    # ======================================
    # Sales Distribution
    # ======================================

    plt.figure(figsize=(8,5))

    plt.hist(data["Sales"], bins=30)

    plt.title("Sales Distribution")

    plt.xlabel("Sales")

    plt.ylabel("Frequency")

    plt.savefig("outputs/sales_distribution.png")

    plt.show()

    # ======================================
    # Profit Distribution
    # ======================================

    plt.figure(figsize=(8,5))

    plt.hist(data["Profit"], bins=30)

    plt.title("Profit Distribution")

    plt.xlabel("Profit")

    plt.ylabel("Frequency")

    plt.savefig("outputs/profit_distribution.png")

    plt.show()

    # ======================================
    # Scatter Plot
    # ======================================

    plt.figure(figsize=(8,6))

    plt.scatter(
        data["Sales"],
        data["Profit"]
    )

    plt.title("Sales vs Profit")

    plt.xlabel("Sales")

    plt.ylabel("Profit")

    plt.savefig("outputs/sales_vs_profit.png")

    plt.show()

    print("\nDashboard Charts Created Successfully.")