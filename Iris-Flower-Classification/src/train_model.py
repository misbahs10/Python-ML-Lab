"""
=========================================================
Description:
Train and evaluate machine learning models for
Iris Flower Classification.
=========================================================
"""

import os
import joblib # type: ignore
import pandas as pd # type: ignore

from sklearn.model_selection import train_test_split, cross_val_score # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore
from sklearn.metrics import ( # type: ignore
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# ==========================================================
# File Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "iris-cleaned.csv")

MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODEL_DIR, "iris_model.pkl")

# ==========================================================
# Load Dataset
# ==========================================================


def load_dataset():

    try:
        data = pd.read_csv(DATA_PATH)

        print("=" * 60)
        print("Clean Dataset Loaded Successfully")
        print("=" * 60)

        return data

    except FileNotFoundError:

        print("Error: iris-cleaned.csv not found.")
        print("Run data_preprocessing.py first.")

        exit()


# ==========================================================
# Prepare Features & Target
# ==========================================================


def prepare_data(data):

    X = data.drop("species", axis=1)

    y = data["species"]

    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )


# ==========================================================
# Train Models
# ==========================================================


def train_models(X_train, X_test, y_train, y_test):

    models = {
        "Logistic Regression": LogisticRegression(max_iter=300),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            random_state=42,
        ),
    }

    best_model = None
    best_accuracy = 0

    print("\nModel Results")
    print("=" * 60)

    for name, model in models.items():

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        print(f"\n{name}")
        print("-" * 40)
        print(f"Accuracy : {accuracy:.4f}")

        print("\nClassification Report")
        print(classification_report(y_test, predictions))

        print("Confusion Matrix")
        print(confusion_matrix(y_test, predictions))

        scores = cross_val_score(model, X_train, y_train, cv=5)

        print(f"Cross Validation Accuracy : {scores.mean():.4f}")

        if accuracy > best_accuracy:

            best_accuracy = accuracy
            best_model = model

    return best_model, best_accuracy


# ==========================================================
# Save Model
# ==========================================================


def save_model(model):

    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print("\nModel Saved Successfully")
    print(MODEL_PATH)


# ==========================================================
# Main Function
# ==========================================================


def main():

    print("=" * 60)
    print("IRIS FLOWER MODEL TRAINING")
    print("=" * 60)

    data = load_dataset()

    X_train, X_test, y_train, y_test = prepare_data(data)

    best_model, accuracy = train_models(
        X_train,
        X_test,
        y_train,
        y_test,
    )

    print("\n" + "=" * 60)
    print(f"Best Model Accuracy : {accuracy:.4f}")
    print("=" * 60)

    save_model(best_model)

    print("\nTraining Completed Successfully")


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":
    main()