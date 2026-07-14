"""
===========================================
Model Evaluation Functions
===========================================
"""

import numpy as np
from sklearn.metrics import (  # type: ignore
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def evaluate_model(model_name, y_test, predictions):
    """
    Evaluate Regression Model
    """

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print("\n" + "=" * 50)
    print(f"Model : {model_name}")
    print("=" * 50)
    print(f"MAE  : {mae:.2f}")
    print(f"MSE  : {mse:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.4f}")

    return r2