"""
=========================================================
Description:
This script performs data preprocessing on the Iris dataset.

Tasks Performed:
1. Load Dataset
2. Display Dataset Information
3. Check Missing Values
4. Check Duplicate Rows
5. Remove Duplicates
6. Display Statistical Summary
7. Save Cleaned Dataset
=========================================================
"""

import os
import pandas as pd # type: ignore


# =========================================================
# File Paths
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "iris.csv")

OUTPUT_PATH = os.path.join(BASE_DIR, "data", "iris-cleaned.csv")


# =========================================================
# Load Dataset
# =========================================================

def load_dataset(path):
    """
    Load CSV dataset.
    """

    try:
        data = pd.read_csv(path)

        print("=" * 60)
        print(" Dataset Loaded Successfully")
        print("=" * 60)

        return data

    except FileNotFoundError:
        print(" Dataset not found.")
        print(path)
        exit()

    except Exception as e:
        print(" Error:", e)
        exit()


# =========================================================
# Dataset Overview
# =========================================================

def dataset_overview(data):

    print("\n First 5 Rows\n")
    print(data.head())

    print("\n Dataset Shape")
    print(data.shape)

    print("\n Column Names")
    print(data.columns.tolist())

    print("\n Data Types")
    print(data.dtypes)

    print("\n Dataset Information")
    print(data.info())


# =========================================================
# Missing Values
# =========================================================

def check_missing_values(data):

    print("\n Missing Values")

    missing = data.isnull().sum()

    print(missing)

    print("\nTotal Missing Values :", missing.sum())


# =========================================================
# Duplicate Values
# =========================================================

def remove_duplicates(data):

    duplicates = data.duplicated().sum()

    print("\n Duplicate Rows :", duplicates)

    if duplicates > 0:

        data = data.drop_duplicates()

        print(" Duplicates Removed Successfully")

    else:

        print(" No Duplicate Rows Found")

    return data


# =========================================================
# Statistical Summary
# =========================================================

def statistical_summary(data):

    print("\n Statistical Summary\n")

    print(data.describe(include="all"))


# =========================================================
# Save Clean Dataset
# =========================================================

def save_dataset(data, path):

    data.to_csv(path, index=False)

    print("\n Clean Dataset Saved Successfully")

    print(path)


# =========================================================
# Main Function
# =========================================================

def main():

    print("=" * 60)
    print("IRIS FLOWER DATA PREPROCESSING")
    print("=" * 60)

    data = load_dataset(DATA_PATH)

    dataset_overview(data)

    check_missing_values(data)

    data = remove_duplicates(data)

    statistical_summary(data)

    save_dataset(data, OUTPUT_PATH)

    print("\n Preprocessing Completed Successfully")


# =========================================================
# Run Program
# =========================================================

if __name__ == "__main__":
    main()