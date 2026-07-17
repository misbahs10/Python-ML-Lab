from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore

from data_preprocessing import preprocess_data
from utils import save_model, calculate_accuracy
from config import MODEL_PATH


def train_models():

    # Load Preprocessed Data
    X_train, X_test, y_train, y_test = preprocess_data()

    print("\n" + "=" * 60)
    print("Training Models...")
    print("=" * 60)

    # ============================
    # Logistic Regression
    # ============================

    logistic_model = LogisticRegression(max_iter=1000)

    logistic_model.fit(X_train, y_train)

    logistic_predictions = logistic_model.predict(X_test)

    logistic_accuracy = calculate_accuracy(
        y_test,
        logistic_predictions
    )

    print(f"\nLogistic Regression Accuracy : {logistic_accuracy:.4f}")

    # ============================
    # Random Forest
    # ============================

    random_forest_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    random_forest_model.fit(X_train, y_train)

    rf_predictions = random_forest_model.predict(X_test)

    rf_accuracy = calculate_accuracy(
        y_test,
        rf_predictions
    )

    print(f"Random Forest Accuracy : {rf_accuracy:.4f}")

    # ============================
    # Compare Models
    # ============================

    if rf_accuracy > logistic_accuracy:

        best_model = random_forest_model
        best_model_name = "Random Forest"
        best_accuracy = rf_accuracy

    else:

        best_model = logistic_model
        best_model_name = "Logistic Regression"
        best_accuracy = logistic_accuracy

    print("\n" + "=" * 60)
    print("Best Model")
    print("=" * 60)

    print(f"Model Name : {best_model_name}")
    print(f"Accuracy   : {best_accuracy:.4f}")

    # ============================
    # Save Model
    # ============================

    save_model(best_model, MODEL_PATH)


if __name__ == "__main__":
    train_models()