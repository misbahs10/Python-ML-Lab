"""
===========================================
House Price Prediction
Prediction Script
===========================================
"""

import pandas as pd
from utils import load_model
from config import MODEL_PATH


def get_user_input():

    print("\n========== Enter House Details ==========\n")

    area = int(input("Area : "))
    bedrooms = int(input("Bedrooms : "))
    bathrooms = int(input("Bathrooms : "))
    stories = int(input("Stories : "))

    mainroad = input("Main Road (yes/no): ").lower()
    guestroom = input("Guest Room (yes/no): ").lower()
    basement = input("Basement (yes/no): ").lower()
    hotwaterheating = input("Hot Water Heating (yes/no): ").lower()
    airconditioning = input("Air Conditioning (yes/no): ").lower()

    parking = int(input("Parking : "))

    prefarea = input("Preferred Area (yes/no): ").lower()

    furnishingstatus = input(
        "Furnishing Status (furnished / semi-furnished / unfurnished): "
    ).lower()

    data = {
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "stories": stories,
        "parking": parking,

        "mainroad_yes": 1 if mainroad == "yes" else 0,
        "guestroom_yes": 1 if guestroom == "yes" else 0,
        "basement_yes": 1 if basement == "yes" else 0,
        "hotwaterheating_yes": 1 if hotwaterheating == "yes" else 0,
        "airconditioning_yes": 1 if airconditioning == "yes" else 0,
        "prefarea_yes": 1 if prefarea == "yes" else 0,

        "furnishingstatus_semi-furnished": 1 if furnishingstatus == "semi-furnished" else 0,
        "furnishingstatus_unfurnished": 1 if furnishingstatus == "unfurnished" else 0
    }

    return pd.DataFrame([data])


def predict_price():

    model = load_model(MODEL_PATH)

    input_data = get_user_input()

    prediction = model.predict(input_data)

    print("\n====================================")
    print(f"Predicted House Price : PKR {prediction[0]:,.0f}")
    print("====================================")


if __name__ == "__main__":
    predict_price()