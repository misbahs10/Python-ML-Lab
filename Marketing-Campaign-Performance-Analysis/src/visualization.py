import os
import pandas as pd #type: ignore
import matplotlib.pyplot as plt
import seaborn as sns #type: ignore

from src.config import GRAPH_DIR


sns.set_theme(
    style="whitegrid"
)


# ==================================
# Save Graph Function
# ==================================

def save_plot(filename):

    path = os.path.join(
        GRAPH_DIR,
        filename
    )

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()



# ==================================
# 1. Campaign Response
# ==================================

def campaign_response(df):

    plt.figure(
        figsize=(8,5)
    )


    sns.countplot(
        data=df,
        x="response"
    )


    plt.title(
        "Marketing Campaign Response",
        fontsize=16,
        fontweight="bold"
    )


    plt.xlabel(
        "Response"
    )


    plt.ylabel(
        "Number of Customers"
    )


    save_plot(
        "campaign_response.png"
    )



# ==================================
# 2. Customer Age Distribution
# ==================================

def customer_age_distribution(df):


    df["age"] = (
        2026 - df["year_birth"]
    )


    plt.figure(
        figsize=(10,5)
    )


    sns.histplot(
        data=df,
        x="age",
        bins=30,
        kde=True
    )


    plt.title(
        "Customer Age Distribution",
        fontsize=16,
        fontweight="bold"
    )


    save_plot(
        "customer_age_distribution.png"
    )



# ==================================
# 3. Income Distribution
# ==================================

def income_distribution(df):


    plt.figure(
        figsize=(10,5)
    )


    sns.histplot(
        data=df,
        x="income",
        bins=40,
        kde=True
    )


    plt.title(
        "Customer Income Distribution",
        fontsize=16,
        fontweight="bold"
    )


    save_plot(
        "income_distribution.png"
    )



# ==================================
# 4. Education Analysis
# ==================================

def education_analysis(df):


    plt.figure(
        figsize=(10,6)
    )


    education = (
        df["education"]
        .value_counts()
        .reset_index()
    )


    education.columns = [
        "education",
        "count"
    ]


    sns.barplot(
        data=education,
        x="count",
        y="education"
    )


    plt.title(
        "Customer Education Level",
        fontsize=16,
        fontweight="bold"
    )


    save_plot(
        "education_analysis.png"
    )



# ==================================
# 5. Product Spending
# ==================================

def spending_analysis(df):


    spending_columns = [

        "mntwines",
        "mntfruits",
        "mntmeatproducts",
        "mntfishproducts",
        "mntsweetproducts",
        "mntgoldprods"

    ]


    spending = (
        df[spending_columns]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    plt.figure(
        figsize=(10,6)
    )


    sns.barplot(
        x=spending.values,
        y=spending.index
    )


    plt.title(
        "Product Category Spending",
        fontsize=16,
        fontweight="bold"
    )


    plt.xlabel(
        "Total Spending"
    )


    save_plot(
        "spending_analysis.png"
    )



# ==================================
# 6. Purchase Channels
# ==================================

def purchase_channels(df):


    channels = {

        "Web":
        df["numwebpurchases"].sum(),

        "Store":
        df["numstorepurchases"].sum(),

        "Catalog":
        df["numcatalogpurchases"].sum()

    }


    plt.figure(
        figsize=(8,5)
    )


    sns.barplot(
        x=list(channels.keys()),
        y=list(channels.values())
    )


    plt.title(
        "Purchase Channel Performance",
        fontsize=16,
        fontweight="bold"
    )


    save_plot(
        "purchase_channels.png"
    )



# ==================================
# 7. Customer Segmentation
# ==================================

def customer_segments(df):


    spending = (

        df["mntwines"]+
        df["mntfruits"]+
        df["mntmeatproducts"]+
        df["mntfishproducts"]+
        df["mntsweetproducts"]+
        df["mntgoldprods"]

    )


    df["segment"] = pd.qcut(
        spending,
        4,
        labels=[
            "Low",
            "Medium",
            "High",
            "Premium"
        ]
    )


    plt.figure(
        figsize=(8,5)
    )


    sns.countplot(
        data=df,
        x="segment"
    )


    plt.title(
        "Customer Segmentation",
        fontsize=16,
        fontweight="bold"
    )


    save_plot(
        "customer_segments.png"
    )



# ==================================
# 8. Correlation Heatmap
# ==================================

def correlation_heatmap(df):

    plt.figure(
        figsize=(16,12)
    )


    corr = (
        df.select_dtypes(
            include="number"
        )
        .corr()
    )


    sns.heatmap(

        corr,

        annot=True,          
        fmt=".2f",           

        cmap="coolwarm",

        center=0,

        linewidths=0.5

    )


    plt.title(
        "Feature Correlation Heatmap",
        fontsize=16,
        fontweight="bold"
    )


    save_plot(
        "correlation_heatmap.png"
    )