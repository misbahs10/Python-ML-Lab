"""
===========================================
House Price Prediction
Model Training
===========================================
"""

from sklearn.linear_model import LinearRegression  # type: ignore
from sklearn.tree import DecisionTreeRegressor  # type: ignore
from sklearn.ensemble import RandomForestRegressor  # type: ignore

# Local imports (may be unresolved by some static analyzers/linters)
from data_preprocessing import preprocess_data  # type: ignore
from evaluate import evaluate_model  # type: ignore
from utils import create_directory, save_model  # type: ignore
from config import MODEL_DIR, MODEL_PATH, RANDOM_STATE  # type: ignore


def train_models():

    # Load Processed Data
    X_train, X_test, y_train, y_test = preprocess_data()

    # Models
    models = {

        "Linear Regression":
            LinearRegression(),

        "Decision Tree":
            DecisionTreeRegressor(
                random_state=RANDOM_STATE
            ),

        "Random Forest":
            RandomForestRegressor(
                n_estimators=100,
                random_state=RANDOM_STATE
            )
    }

    best_model = None
    best_score = -999

    for model_name, model in models.items():

        print("\nTraining:", model_name)

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        score = evaluate_model(
            model_name,
            y_test,
            predictions
        )

        if score > best_score:
            best_score = score
            best_model = model

    create_directory(MODEL_DIR)

    save_model(best_model, MODEL_PATH)

    print("\n" + "=" * 50)
    print("Best Model Saved Successfully")
    print(f"R² Score : {best_score:.4f}")
    print("=" * 50)


if __name__ == "__main__":
    train_models()