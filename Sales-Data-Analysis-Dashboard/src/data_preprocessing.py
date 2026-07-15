"""
============================================
Sales Data Analysis Dashboard
Data Preprocessing
============================================
"""

import pandas as pd # type: ignore

from src.config import DATA_PATH
from src.utils import load_data


def preprocess_data():

    # Load Dataset
    data = load_data(DATA_PATH)

    if data is None:
        return

    print("\n" + "=" * 60)
    print("FIRST 5 ROWS")
    print("=" * 60)
    print(data.head())

    print("\n" + "=" * 60)
    print("DATASET SHAPE")
    print("=" * 60)
    print(data.shape)

    print("\n" + "=" * 60)
    print("COLUMN NAMES")
    print("=" * 60)
    print(data.columns.tolist())

    print("\n" + "=" * 60)
    print("DATA TYPES")
    print("=" * 60)
    print(data.dtypes)

    print("\n" + "=" * 60)
    print("DATASET INFORMATION")
    print("=" * 60)
    data.info()

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)
    print(data.isnull().sum())

    print("\n" + "=" * 60)
    print("TOTAL MISSING VALUES")
    print("=" * 60)
    print(data.isnull().sum().sum())

    print("\n" + "=" * 60)
    print("DUPLICATE RECORDS")
    print("=" * 60)
    print(data.duplicated().sum())

    # Remove Duplicates
    data = data.drop_duplicates()

    # Convert Date Columns
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    data["Ship Date"] = pd.to_datetime(data["Ship Date"])

    print("\nDate columns converted successfully.")

    # Create Month Column
    data["Month"] = data["Order Date"].dt.month_name()

    # Create Year Column
    data["Year"] = data["Order Date"].dt.year

    # Save Clean Dataset
    data.to_csv("outputs/cleaned_sales_data.csv", index=False)

    print("\nCleaned Dataset Saved Successfully.")

    return data


if __name__ == "__main__":
    preprocess_data()