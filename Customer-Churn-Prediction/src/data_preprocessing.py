"""
=========================================================
CUSTOMER CHURN DATA PREPROCESSING
=========================================================
"""

import pandas as pd #type: ignore
import joblib #type: ignore
from sklearn.preprocessing import LabelEncoder #type: ignore

from config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    FEATURE_COLUMNS_PATH,
)

from utils import print_header, print_success


def load_data():
    """Load dataset"""

    print_header("Loading Dataset")

    data = pd.read_csv(RAW_DATA_PATH)

    print_success("Dataset Loaded Successfully")

    return data


def dataset_information(data):
    """Display dataset information"""

    print_header("Dataset Information")

    print(f"Shape : {data.shape}\n")

    print("Columns:")
    print(data.columns.tolist())

    print("\nData Types:")
    print(data.dtypes)

    print("\nFirst 5 Rows")
    print(data.head())


def check_missing_values(data):
    """Check missing values"""

    print_header("Missing Values")

    missing = data.isnull().sum()

    print(missing)

    print(f"\nTotal Missing Values : {missing.sum()}")


def remove_duplicates(data):
    """Remove duplicate rows"""

    print_header("Duplicate Values")

    duplicates = data.duplicated().sum()

    print(f"Duplicate Rows : {duplicates}")

    if duplicates > 0:
        data = data.drop_duplicates()
        print_success("Duplicates Removed")

    return data


def clean_total_charges(data):
    """Convert TotalCharges into numeric"""

    print_header("Cleaning TotalCharges")

    data["TotalCharges"] = data["TotalCharges"].replace(" ", pd.NA)

    data["TotalCharges"] = pd.to_numeric(
        data["TotalCharges"],
        errors="coerce"
    )

    data["TotalCharges"] = data["TotalCharges"].fillna(
        data["TotalCharges"].median()
    )

    print_success("TotalCharges Cleaned")

    return data


def drop_customer_id(data):
    """Remove customerID"""

    print_header("Dropping customerID")

    data = data.drop(columns=["customerID"])

    print_success("customerID Removed")

    return data


def encode_target(data):
    """Encode Churn Column"""

    print_header("Encoding Target")

    encoder = LabelEncoder()

    data["Churn"] = encoder.fit_transform(data["Churn"])

    print_success("Target Encoded")

    return data


def encode_features(data):
    """One-Hot Encoding"""

    print_header("Encoding Features")

    categorical_columns = data.select_dtypes(
    include=["object", "string"]
    ).columns.tolist()

    data = pd.get_dummies(
        data,
        columns=categorical_columns,
        drop_first=True
    )

    print_success("Categorical Features Encoded")

    return data


def save_dataset(data):
    """Save cleaned dataset"""

    print_header("Saving Dataset")

    data.to_csv(PROCESSED_DATA_PATH, index=False)

    print_success(f"Dataset Saved Successfully")

    print(PROCESSED_DATA_PATH)


def main():

    data = load_data()

    dataset_information(data)

    check_missing_values(data)

    data = remove_duplicates(data)

    data = clean_total_charges(data)

    data = drop_customer_id(data)

    data = encode_target(data)

    data = encode_features(data)

    # =====================================================
    # Save Feature Columns
    # =====================================================

    feature_columns = data.drop(
        "Churn",
        axis=1
    ).columns.tolist()

    joblib.dump(
        feature_columns,
        FEATURE_COLUMNS_PATH
    )

    print_success("Feature Columns Saved Successfully")

    # =====================================================
    # Save Dataset
    # =====================================================

    save_dataset(data)

    print_header("Preprocessing Completed")

# =====================================================
# Run Script
# =====================================================

if __name__ == "__main__":
    main()