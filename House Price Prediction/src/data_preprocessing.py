"""
===========================================
House Price Prediction
Data Preprocessing
===========================================
"""

import pandas as pd  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore

try:
    import config  # type: ignore
except Exception:  # pragma: no cover - fallback when config is missing
    import os

    print("⚠️  'config' module not found. Falling back to default settings.")

    class Config:
        """Simple configuration class used when a config module is not present.

        Provides getter methods for all settings so callers can rely on
        attributes or method access.
        """

        def __init__(self) -> None:
            self.DATA_PATH = os.getenv("DATA_PATH", "housing.csv")
            try:
                self.TEST_SIZE = float(os.getenv("TEST_SIZE", 0.2))
            except Exception:
                self.TEST_SIZE = 0.2
            try:
                self.RANDOM_STATE = int(os.getenv("RANDOM_STATE", 42))
            except Exception:
                self.RANDOM_STATE = 42

        def get_data_path(self) -> str:
            """Return the path to the dataset."""
            return self.DATA_PATH

        def get_test_size(self) -> float:
            """Return the test set fraction."""
            return self.TEST_SIZE

        def get_random_state(self) -> int:
            """Return the random state used for reproducibility."""
            return self.RANDOM_STATE

    config = Config()


def load_data():
    """
    Load Housing Dataset
    """
    try:
        data = pd.read_csv(config.DATA_PATH)
        print("✅ Dataset Loaded Successfully.")
        return data
    except FileNotFoundError:
        print("❌ Housing.csv not found!")
        return None


def explore_data(data):
    """
    Display Dataset Information
    """
    print("\n========== First 5 Rows ==========")
    print(data.head())

    print("\n========== Dataset Shape ==========")
    print(data.shape)

    print("\n========== Dataset Info ==========")
    print(data.info())

    print("\n========== Missing Values ==========")
    print(data.isnull().sum())

    print("\n========== Duplicate Rows ==========")
    print(data.duplicated().sum())


def clean_data(data):
    """
    Clean Dataset
    """

    # Remove Duplicate Rows
    data = data.drop_duplicates()

    # Fill Missing Values
    for column in data.columns:

        if data[column].dtype == "object":
            data[column] = data[column].fillna(data[column].mode()[0])

        else:
            data[column] = data[column].fillna(data[column].median())

    print("\n✅ Data Cleaning Completed.")

    return data


def encode_data(data):
    """
    Convert Categorical Columns into Numeric
    """

    categorical_columns = data.select_dtypes(include="object").columns

    data = pd.get_dummies(
        data,
        columns=categorical_columns,
        drop_first=True
    )

    print("✅ Encoding Completed.")

    return data


def split_data(data):
    """
    Split Features and Target
    """

    X = data.drop("price", axis=1)

    y = data["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE
    )

    print("✅ Train-Test Split Completed.")

    return X_train, X_test, y_train, y_test


def preprocess_data():
    """
    Complete Preprocessing Pipeline
    """

    data = load_data()

    if data is None:
        return None

    explore_data(data)

    data = clean_data(data)

    data = encode_data(data)

    X_train, X_test, y_train, y_test = split_data(data)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":

    preprocess_data()