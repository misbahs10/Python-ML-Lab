"""
=========================================================
Predict Iris Flower Species
=========================================================
"""

import os
import pandas as pd # type: ignore

from utils import load_model, get_float_input

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "iris_model.pkl"
)

# ==========================================================
# Main
# ==========================================================


def main():

    print("=" * 60)
    print("🌸 IRIS FLOWER SPECIES PREDICTION")
    print("=" * 60)

    model = load_model(MODEL_PATH)

    print("\nEnter Flower Measurements\n")

    sepal_length = get_float_input("Sepal Length (cm) : ")
    sepal_width = get_float_input("Sepal Width (cm)  : ")
    petal_length = get_float_input("Petal Length (cm) : ")
    petal_width = get_float_input("Petal Width (cm)  : ")

    sample = pd.DataFrame(
        [[
            sepal_length,
            sepal_width,
            petal_length,
            petal_width
        ]],
        columns=[
            "sepal_length",
            "sepal_width",
            "petal_length",
            "petal_width"
        ]
    )

    prediction = model.predict(sample)[0]

    print("\n" + "=" * 60)
    print(f"Predicted Species : {prediction}")

    if hasattr(model, "predict_proba"):

        probability = model.predict_proba(sample).max() * 100

        print(f"Confidence Score : {probability:.2f}%")

    print("=" * 60)


if __name__ == "__main__":
    main()