# ============================================
# Student Performance Prediction
# Utility Functions
# ============================================

import pandas as pd # type: ignore
import joblib # type: ignore

# ============================================
# Load Dataset
# ============================================

def load_dataset(file_path):
    """
    Load CSV dataset
    """

    data = pd.read_csv(file_path)

    return data


# ============================================
# Load Trained Model
# ============================================

def load_model(model_path):

    model = joblib.load(model_path)

    return model


# ============================================
# Load Encoders
# ============================================

def load_encoders(encoder_path):

    encoders = joblib.load(encoder_path)

    return encoders


# ============================================
# Display Dataset Information
# ============================================

def dataset_info(data):

    print("=" * 60)
    print("Dataset Shape")
    print("=" * 60)
    print(data.shape)

    print("\n" + "=" * 60)
    print("Column Names")
    print("=" * 60)
    print(data.columns)

    print("\n" + "=" * 60)
    print("Missing Values")
    print("=" * 60)
    print(data.isnull().sum())

    print("\n" + "=" * 60)
    print("Duplicate Rows")
    print("=" * 60)
    print(data.duplicated().sum())


# ============================================
# Clean Missing Values
# ============================================

def clean_missing_values(data):

    numeric_columns = data.select_dtypes(include=["number"]).columns

    for col in numeric_columns:

        data[col] = data[col].fillna(data[col].median())

    categorical_columns = data.select_dtypes(include=["object"]).columns

    for col in categorical_columns:

        data[col] = data[col].fillna(data[col].mode()[0])

    return data


# ============================================
# Create Performance Column
# ============================================

def create_performance(score):

    if score < 60:

        return "Poor"

    elif score < 80:

        return "Average"

    else:

        return "Excellent"


# ============================================
# Predict Performance
# ============================================

def predict_student(model, input_data):

    prediction = model.predict(input_data)

    return prediction


# ============================================
# Save Clean Dataset
# ============================================

def save_dataset(data, file_path):

    data.to_csv(file_path, index=False)

    print(f"Dataset Saved Successfully : {file_path}")