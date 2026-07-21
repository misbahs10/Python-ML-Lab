"""
============================================================
CUSTOMER CHURN PREDICTION
PREDICTION SCRIPT
============================================================
"""

import joblib #type: ignore
import pandas as pd #type: ignore

from config import (
    MODEL_PATH,
    FEATURE_COLUMNS_PATH,
)

from utils import (
    print_header,
    print_success,
)


# ============================================================
# Load Model & Feature Columns
# ============================================================

def load_artifacts():

    print_header("LOADING MODEL")

    model = joblib.load(MODEL_PATH)

    feature_columns = joblib.load(
        FEATURE_COLUMNS_PATH
    )

    print_success("Model Loaded Successfully")

    print_success("Feature Columns Loaded Successfully")

    return model, feature_columns


# ============================================================
# Get Customer Details
# ============================================================

def get_customer_details():

    print_header("ENTER CUSTOMER DETAILS")

    customer = {}

    customer["gender"] = input(
        "Gender (Male/Female): "
    )

    customer["SeniorCitizen"] = int(
        input("Senior Citizen (0/1): ")
    )

    customer["Partner"] = input(
        "Partner (Yes/No): "
    )

    customer["Dependents"] = input(
        "Dependents (Yes/No): "
    )

    customer["tenure"] = int(
        input("Tenure (Months): ")
    )

    customer["PhoneService"] = input(
        "Phone Service (Yes/No): "
    )

    customer["MultipleLines"] = input(
        "Multiple Lines (Yes/No/No phone service): "
    )

    customer["InternetService"] = input(
        "Internet Service (DSL/Fiber optic/No): "
    )

    customer["OnlineSecurity"] = input(
        "Online Security (Yes/No/No internet service): "
    )

    customer["OnlineBackup"] = input(
        "Online Backup (Yes/No/No internet service): "
    )

    customer["DeviceProtection"] = input(
        "Device Protection (Yes/No/No internet service): "
    )

    customer["TechSupport"] = input(
        "Tech Support (Yes/No/No internet service): "
    )

    customer["StreamingTV"] = input(
        "Streaming TV (Yes/No/No internet service): "
    )

    customer["StreamingMovies"] = input(
        "Streaming Movies (Yes/No/No internet service): "
    )

    customer["Contract"] = input(
        "Contract (Month-to-month/One year/Two year): "
    )

    customer["PaperlessBilling"] = input(
        "Paperless Billing (Yes/No): "
    )

    customer["PaymentMethod"] = input(
        "Payment Method: "
    )

    customer["MonthlyCharges"] = float(
        input("Monthly Charges: ")
    )

    customer["TotalCharges"] = float(
        input("Total Charges: ")
    )

    customer_df = pd.DataFrame(
        [customer]
    )

    print_success(
        "Customer Details Collected Successfully"
    )

    return customer_df

# ============================================================
# Preprocess Customer Data
# ============================================================

def preprocess_customer_data(
    customer_df,
    feature_columns,
):
    """
    Apply the same preprocessing used during training
    """

    print_header("PREPROCESSING CUSTOMER DATA")

    # --------------------------------------------------------
    # One-Hot Encoding
    # --------------------------------------------------------

    customer_df = pd.get_dummies(
        customer_df,
        drop_first=True,
    )

    # --------------------------------------------------------
    # Add Missing Columns
    # --------------------------------------------------------

    for column in feature_columns:

        if column not in customer_df.columns:

            customer_df[column] = 0

    # --------------------------------------------------------
    # Remove Extra Columns
    # --------------------------------------------------------

    customer_df = customer_df[
        feature_columns
    ]

    print_success(
        "Customer Data Preprocessed Successfully"
    )

    return customer_df

# ============================================================
# Predict Customer Churn
# ============================================================

def predict_customer(
    model,
    customer_df,
):
    """
    Predict Customer Churn
    """

    print_header("CUSTOMER CHURN PREDICTION")

    prediction = model.predict(customer_df)[0]

    probability = model.predict_proba(customer_df)[0][1]

    retention = 1 - probability

    # --------------------------------------------------------
    # Risk Level
    # --------------------------------------------------------

    if probability < 0.30:

        risk = "LOW 🟢"

    elif probability < 0.70:

        risk = "MEDIUM 🟡"

    else:

        risk = "HIGH 🔴"

    # --------------------------------------------------------
    # Prediction Result
    # --------------------------------------------------------

    print("=" * 60)

    if prediction == 1:

        print("Prediction           : Customer Will Churn")

    else:

        print("Prediction           : Customer Will Stay")

    print(f"Churn Probability    : {probability*100:.2f}%")

    print(f"Retention Probability: {retention*100:.2f}%")

    print(f"Risk Level           : {risk}")

    print("=" * 60)

    print_success("Prediction Completed Successfully")


# ============================================================
# Main Function
# ============================================================

def main():

    # Load model & feature columns
    model, feature_columns = load_artifacts()

    # Get customer details
    customer_df = get_customer_details()

    # Apply preprocessing
    customer_df = preprocess_customer_data(
        customer_df,
        feature_columns,
    )

    # Predict
    predict_customer(
        model,
        customer_df,
    )


# ============================================================
# Run Project
# ============================================================

if __name__ == "__main__":

    main()