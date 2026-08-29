"""
visualization.py
------------------
Generates a meaningful chart from the dataset (Step 4).
Chart: Attrition rate (%) by Department - a bar chart.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd


def generate_attrition_chart(df: pd.DataFrame, output_path: str = "charts/attrition_by_department.png") -> str:
    """
    Create a bar chart showing attrition rate (%) for each department.
    Saves the chart as a PNG file and returns the file path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    attrition_rate = (
        df[df["Attrition"] == "Yes"]
        .groupby("Department")
        .size()
        / df.groupby("Department").size()
        * 100
    ).round(2)

    attrition_rate = attrition_rate.sort_values(ascending=False)

    colors = ["#e74c3c", "#f39c12", "#3498db"]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(attrition_rate.index, attrition_rate.values, color=colors[: len(attrition_rate)])

    # Data labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.3,
            f"{height}%",
            ha="center",
            fontsize=10,
            fontweight="bold",
        )

    plt.title("Employee Attrition Rate by Department", fontsize=14, fontweight="bold")
    plt.xlabel("Department", fontsize=11)
    plt.ylabel("Attrition Rate (%)", fontsize=11)
    plt.ylim(0, max(attrition_rate.values) + 5)
    plt.tight_layout()

    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path