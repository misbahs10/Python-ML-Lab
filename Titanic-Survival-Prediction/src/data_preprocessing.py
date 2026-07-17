import pandas as pd # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from config import DATA_PATH


def load_data():
    """
    Load Titanic Dataset
    """
    data = pd.read_csv(DATA_PATH)
    return data


def preprocess_data():
    """
    Data Cleaning and Preprocessing
    """

    # Load Dataset
    data = load_data()

    print("=" * 50)
    print("Dataset Loaded Successfully")
    print("=" * 50)

    # Shape
    print("\nShape:")
    print(data.shape)

    # Information
    print("\nDataset Info:")
    print(data.info())

    # Missing Values
    print("\nMissing Values:")
    print(data.isnull().sum())

    # ----------------------------
    # Drop Unnecessary Columns
    # ----------------------------
    columns_to_drop = [
        "PassengerId",
        "Name",
        "Ticket",
        "Cabin"
    ]

    data.drop(columns=columns_to_drop, inplace=True)

    # ----------------------------
    # Fill Missing Values
    # ----------------------------

    # Age
    data["Age"] = data["Age"].fillna(data["Age"].median())

    # Embarked
    data["Embarked"] = data["Embarked"].fillna(data["Embarked"].mode()[0])

    # ----------------------------
    # Convert Categorical Columns
    # ----------------------------

    data["Sex"] = data["Sex"].map({
        "male": 0,
        "female": 1
    })

    embarked_mapping = {
        "S": 0,
        "C": 1,
        "Q": 2
    }

    data["Embarked"] = data["Embarked"].map(embarked_mapping)

    # ----------------------------
    # Features and Target
    # ----------------------------

    X = data.drop("Survived", axis=1)

    y = data["Survived"]

    # ----------------------------
    # Train Test Split
    # ----------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("\nPreprocessing Completed Successfully")

    print("\nTraining Shape :", X_train.shape)
    print("Testing Shape :", X_test.shape)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    preprocess_data()