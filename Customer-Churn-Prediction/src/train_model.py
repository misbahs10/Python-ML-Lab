"""
============================================================
CUSTOMER CHURN PREDICTION
MODEL TRAINING
============================================================
"""

import pandas as pd # type: ignore
import joblib # type: ignore

import matplotlib.pyplot as plt # type: ignore
from config import GRAPH_DIR, RAW_DATA_PATH

from sklearn.model_selection import train_test_split # type: ignore

from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.tree import DecisionTreeClassifier # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore

from sklearn.metrics import ( # type: ignore
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
)

from config import (
    PROCESSED_DATA_PATH,
    MODEL_PATH,
    REPORT_PATH,
    RANDOM_STATE,
    TEST_SIZE,
)

from utils import (
    print_header,
    print_success,
)

from visualization import generate_visualizations

# ============================================================
# Load Dataset
# ============================================================

def load_dataset():
    """
    Load Clean Dataset
    """

    print_header("LOADING CLEAN DATASET")

    data = pd.read_csv(PROCESSED_DATA_PATH)

    print_success("Clean Dataset Loaded Successfully")

    return data


# ============================================================
# Train Test Split
# ============================================================

def split_dataset(data):
    """
    Split Dataset into Train & Test
    """

    print_header("TRAIN TEST SPLIT")

    X = data.drop("Churn", axis=1)

    y = data["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print_success("Train Test Split Completed")

    print(f"\nTraining Samples : {len(X_train)}")
    print(f"Testing Samples  : {len(X_test)}")

    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )
# ============================================================
# Train Models
# ============================================================

def train_models(X_train, y_train):
    """
    Train Multiple Machine Learning Models
    """

    print_header("TRAINING MODELS")

    models = {

        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE,
        ),

        "Decision Tree": DecisionTreeClassifier(
            random_state=RANDOM_STATE,
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            random_state=RANDOM_STATE,
        ),
    }

    trained_models = {}

    for name, model in models.items():

        model.fit(X_train, y_train)

        trained_models[name] = model

        print_success(f"{name} Trained Successfully")

    return trained_models


# ============================================================
# Evaluate Models
# ============================================================

def evaluate_models(models, X_test, y_test):
    """
    Evaluate All Models
    """

    print_header("MODEL EVALUATION")

    best_model = None
    best_name = ""
    best_accuracy = 0

    report = ""

    for name, model in models.items():

        predictions = model.predict(X_test)

        probabilities = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        precision = precision_score(
            y_test,
            predictions,
        )

        recall = recall_score(
            y_test,
            predictions,
        )

        f1 = f1_score(
            y_test,
            predictions,
        )

        roc_auc = roc_auc_score(
            y_test,
            probabilities,
        )

        print("\n" + "=" * 60)
        print(name)
        print("=" * 60)

        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")
        print(f"ROC AUC  : {roc_auc:.4f}")

        class_report = classification_report(
            y_test,
            predictions,
        )

        print("\nClassification Report\n")
        print(class_report)

        report += "=" * 70 + "\n"
        report += f"{name}\n"
        report += "=" * 70 + "\n"

        report += f"Accuracy : {accuracy:.4f}\n"
        report += f"Precision: {precision:.4f}\n"
        report += f"Recall   : {recall:.4f}\n"
        report += f"F1 Score : {f1:.4f}\n"
        report += f"ROC AUC  : {roc_auc:.4f}\n\n"

        report += class_report
        report += "\n\n"

        if accuracy > best_accuracy:

            best_accuracy = accuracy
            best_model = model
            best_name = name

    print_header("BEST MODEL")

    print(f"Model Name : {best_name}")
    print(f"Accuracy   : {best_accuracy:.4f}")

    return (
        best_model,
        best_name,
        report,
    )

# ============================================================
# Main Function
# ============================================================

def main():

    print_header("CUSTOMER CHURN MODEL TRAINING")

    # ---------------------------------------------
    # Load Dataset
    # ---------------------------------------------

    data = load_dataset()

    # ---------------------------------------------
    # Split Dataset
    # ---------------------------------------------

    X_train, X_test, y_train, y_test = split_dataset(
        data
    )

    # ---------------------------------------------
    # Train Models
    # ---------------------------------------------

    trained_models = train_models(
        X_train,
        y_train,
    )

    # ---------------------------------------------
    # Evaluate Models
    # ---------------------------------------------

    best_model, best_name, report = evaluate_models(
        trained_models,
        X_test,
        y_test,
    )

    # ---------------------------------------------
    # Save Best Model
    # ---------------------------------------------

    joblib.dump(
        best_model,
        MODEL_PATH,
    )

    print_success(
        f"{best_name} Saved Successfully"
    )

    # ---------------------------------------------
    # Save Model Report
    # ---------------------------------------------

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(report)

    print_success(
        "Model Report Saved Successfully"
    )

    # ---------------------------------------------
    # Generate Visualizations
    # ---------------------------------------------

    generate_visualizations(
        data=data,
        model=best_model,
        X_test=X_test,
        y_test=y_test,
    )

    # ---------------------------------------------
    # Final Message
    # ---------------------------------------------

    print_header("PROJECT COMPLETED")

    print_success(
        "Customer Churn Prediction Model Ready"
    )

    print(f"\nBest Model : {best_name}")

    print(f"Model File : {MODEL_PATH}")

    print(f"Report File: {REPORT_PATH}")

    print(f"Graphs Path: {GRAPH_DIR}")


# ============================================================
# Run Project
# ============================================================

if __name__ == "__main__":

    main()