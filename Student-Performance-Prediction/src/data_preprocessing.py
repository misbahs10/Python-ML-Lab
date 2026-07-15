# ============================================
# Student Performance Prediction
# Data Preprocessing
# ============================================

# Import Libraries
import pandas as pd # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.preprocessing import LabelEncoder # type: ignore


def load_data(file_path):
    """
    Load dataset
    """
    data = pd.read_csv(file_path)
    return data


def explore_data(data):
    """
    Display basic dataset information
    """
    print("=" * 50)
    print("First 5 Rows")
    print("=" * 50)
    print(data.head())

    print("\n" + "=" * 50)
    print("Dataset Shape")
    print("=" * 50)
    print(data.shape)

    print("\n" + "=" * 50)
    print("Column Names")
    print("=" * 50)
    print(data.columns)

    print("\n" + "=" * 50)
    print("Dataset Info")
    print("=" * 50)
    print(data.info())

    print("\n" + "=" * 50)
    print("Statistical Summary")
    print("=" * 50)
    print(data.describe())


def check_missing_values(data):
    """
    Check missing values
    """
    print("\n" + "=" * 50)
    print("Missing Values")
    print("=" * 50)
    print(data.isnull().sum())


def check_duplicates(data):
    """
    Check duplicate values
    """
    duplicates = data.duplicated().sum()

    print("\n" + "=" * 50)
    print("Duplicate Records")
    print("=" * 50)
    print(duplicates)


def clean_data(data):
    """
    Handle Missing Values
    """

    # Numeric Columns
    numeric_columns = data.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_columns:
        data[col].fillna(data[col].median(), inplace=True)

    # Categorical Columns
    categorical_columns = data.select_dtypes(include=["object"]).columns

    for col in categorical_columns:
        data[col].fillna(data[col].mode()[0], inplace=True)

    return data


def encode_data(data):
    """
    Encode Categorical Columns
    """

    encoder = LabelEncoder()

    categorical_columns = data.select_dtypes(include=["object"]).columns

    for col in categorical_columns:
        data[col] = encoder.fit_transform(data[col])

    return data


def split_data(data):

    target_column = "Exam_Score"

    X = data.drop(target_column, axis=1)
    y = data[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":

    dataset_path = "data/student_data.csv"

    data = load_data(dataset_path)

    explore_data(data)

    check_missing_values(data)

    check_duplicates(data)

    data = clean_data(data)

    data = encode_data(data)

    X_train, X_test, y_train, y_test = split_data(data)

    print("\nData Preprocessing Completed Successfully!")

    print("\nTraining Data Shape :", X_train.shape)
    print("Testing Data Shape :", X_test.shape)