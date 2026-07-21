"""
============================================================
CUSTOMER CHURN PREDICTION
VISUALIZATIONS
============================================================
"""

import pandas as pd #type: ignore
import matplotlib.pyplot as plt
import seaborn as sns #type: ignore

from sklearn.metrics import ( # type: ignore
    confusion_matrix,
    roc_curve,
    auc,
)

import numpy as np

from config import (
    GRAPH_DIR,
    RAW_DATA_PATH,
)

from utils import (
    print_header,
    print_success,
)


# ============================================================
# Professional Theme
# ============================================================

sns.set_theme(
    style="whitegrid",
    palette="Set2",
    font_scale=1.1,
)


# ============================================================
# Generate Visualizations
# ============================================================

def generate_visualizations(
    data,
    model,
    X_test,
    y_test,
):
    """
    Generate Professional Visualizations
    """

    print_header("GENERATING VISUALIZATIONS")

    raw_data = pd.read_csv(RAW_DATA_PATH)

    # ============================================================
    # Churn Distribution
    # ============================================================

    plt.figure(figsize=(8, 6))

    ax = sns.countplot(
        data=raw_data,
        x="Churn",
        palette="Set2",
    )

    plt.title(
        "Customer Churn Distribution",
        fontsize=16,
        fontweight="bold",
    )

    plt.xlabel("Churn")

    plt.ylabel("Customers")

    for container in ax.containers:
        ax.bar_label(
            container,
            fontsize=10,
        )

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "churn_distribution.png",
        dpi=300,
    )

    plt.close()

    # ============================================================
    # Monthly Charges Distribution
    # ============================================================

    plt.figure(figsize=(9, 6))

    sns.histplot(
        raw_data["MonthlyCharges"],
        bins=30,
        kde=True,
        color="royalblue",
    )

    plt.title(
        "Monthly Charges Distribution",
        fontsize=16,
        fontweight="bold",
    )

    plt.xlabel("Monthly Charges")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "monthly_charges_distribution.png",
        dpi=300,
    )

    plt.close()

    # ============================================================
    # Tenure Distribution
    # ============================================================

    plt.figure(figsize=(9, 6))

    sns.histplot(
        raw_data["tenure"],
        bins=30,
        kde=True,
        color="darkorange",
    )

    plt.title(
        "Customer Tenure Distribution",
        fontsize=16,
        fontweight="bold",
    )

    plt.xlabel("Tenure (Months)")

    plt.ylabel("Customers")

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "tenure_distribution.png",
        dpi=300,
    )

    plt.close()

    print_success("Basic Graphs Saved Successfully")

    # ============================================================
    # Monthly Charges Boxplot
    # ============================================================

    plt.figure(figsize=(9, 6))

    sns.boxplot(
        x=raw_data["MonthlyCharges"],
        color="skyblue",
        linewidth=2,
        fliersize=3,
    )

    plt.title(
        "Monthly Charges Boxplot",
        fontsize=16,
        fontweight="bold",
    )

    plt.xlabel("Monthly Charges")

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "boxplot_monthlycharges.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    # ============================================================
    # Contract vs Churn
    # ============================================================

    plt.figure(figsize=(10, 6))

    ax = sns.countplot(
        data=raw_data,
        x="Contract",
        hue="Churn",
        palette="Set2",
    )

    plt.title(
        "Contract Type vs Customer Churn",
        fontsize=16,
        fontweight="bold",
    )

    plt.xlabel("Contract Type")

    plt.ylabel("Customers")

    plt.xticks(rotation=15)

    for container in ax.containers:
        ax.bar_label(
            container,
            fontsize=9,
        )

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "contract_vs_churn.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    # ============================================================
    # Internet Service vs Churn
    # ============================================================

    plt.figure(figsize=(10, 6))

    ax = sns.countplot(
        data=raw_data,
        x="InternetService",
        hue="Churn",
        palette="viridis",
    )

    plt.title(
        "Internet Service vs Customer Churn",
        fontsize=16,
        fontweight="bold",
    )

    plt.xlabel("Internet Service")

    plt.ylabel("Customers")

    plt.xticks(rotation=10)

    for container in ax.containers:
        ax.bar_label(
            container,
            fontsize=9,
        )

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "internet_service_vs_churn.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    # ============================================================
    # Correlation Heatmap
    # ============================================================

    plt.figure(figsize=(18, 12))

    correlation = data.corr(numeric_only=True)

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        linewidths=0.5,
        square=False,
        cbar=True,
    )

    plt.title(
        "Feature Correlation Heatmap",
        fontsize=18,
        fontweight="bold",
    )

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "correlation_heatmap.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print_success("Advanced Graphs Saved Successfully")

    # ============================================================
    # Confusion Matrix
    # ============================================================

    predictions = model.predict(X_test)

    cm = confusion_matrix(
        y_test,
        predictions
    )

    plt.figure(figsize=(7, 6))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
    )

    plt.title(
        "Confusion Matrix",
        fontsize=16,
        fontweight="bold",
    )

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "confusion_matrix.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    # ============================================================
    # ROC Curve
    # ============================================================

    probability = model.predict_proba(X_test)[:, 1]

    fpr, tpr, _ = roc_curve(
        y_test,
        probability,
    )

    roc_auc = auc(
        fpr,
        tpr,
    )

    plt.figure(figsize=(7, 6))

    plt.plot(
        fpr,
        tpr,
        linewidth=3,
        label=f"AUC = {roc_auc:.3f}",
    )

    plt.plot(
        [0, 1],
        [0, 1],
        "--",
        linewidth=2,
    )

    plt.xlabel("False Positive Rate")

    plt.ylabel("True Positive Rate")

    plt.title(
        "ROC Curve",
        fontsize=16,
        fontweight="bold",
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "roc_curve.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    # ============================================================
    # Feature Importance
    # ============================================================

    if hasattr(model, "feature_importances_"):

        importance = pd.Series(
            model.feature_importances_,
            index=X_test.columns,
        )

        importance = (
            importance
            .sort_values(ascending=False)
            .head(15)
        )

        plt.figure(figsize=(10, 7))

        sns.barplot(
            x=importance.values,
            y=importance.index,
            palette="viridis",
        )

        plt.title(
            "Top 15 Feature Importance",
            fontsize=16,
            fontweight="bold",
        )

        plt.xlabel("Importance Score")

        plt.ylabel("Features")

        plt.tight_layout()

        plt.savefig(
            GRAPH_DIR / "feature_importance.png",
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

    # ============================================================
    # Pairplot (Optimized)
    # ============================================================

    pairplot_columns = [
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "Churn",
    ]

    available_columns = [
        column
        for column in pairplot_columns
        if column in data.columns
    ]

    if len(available_columns) == 4:

        sample = data.sample(
            min(300, len(data)),
            random_state=42,
        )

        pair = sns.pairplot(
            sample[available_columns],
            hue="Churn",
            corner=True,
            diag_kind="hist",
        )

        pair.figure.savefig(
            GRAPH_DIR / "pairplot.png",
            dpi=300,
            bbox_inches="tight",
        )

        plt.close("all")

    print_success("All Graphs Saved Successfully")