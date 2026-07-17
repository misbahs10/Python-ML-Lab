import pandas as pd # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore

from utils import load_model
from config import MODEL_PATH


# Load Saved Model
model = load_model(MODEL_PATH)

print("=" * 50)
print("Titanic Survival Prediction")
print("=" * 50)

# ----------------------------
# User Input
# ----------------------------

pclass = int(input("Passenger Class (1,2,3): "))

gender = input("Gender (male/female): ").strip().lower()

age = float(input("Age: "))

sibsp = int(input("Number of Siblings/Spouses: "))

parch = int(input("Number of Parents/Children: "))

fare = float(input("Fare: "))

embarked = input("Embarked (S/C/Q): ").strip().upper()

# ----------------------------
# Encoding
# ----------------------------

if gender == "male":
    gender = 0
else:
    gender = 1

embarked_mapping = {
    "S": 0,
    "C": 1,
    "Q": 2
}

embarked = embarked_mapping.get(embarked, 0)

# ----------------------------
# Create DataFrame
# ----------------------------

input_data = pd.DataFrame({
    "Pclass": [pclass],
    "Sex": [gender],
    "Age": [age],
    "SibSp": [sibsp],
    "Parch": [parch],
    "Fare": [fare],
    "Embarked": [embarked]
})

# ----------------------------
# Prediction
# ----------------------------

prediction = model.predict(input_data)

print("\n" + "=" * 50)

if prediction[0] == 1:
    print("Prediction : Passenger Survived")
else:
    print("Prediction : Passenger Not Survived")

# ----------------------------
# Prediction Probability
# ----------------------------

if hasattr(model, "predict_proba"):

    probability = model.predict_proba(input_data)

    print("\nSurvival Probability")

    print(f"Not Survived : {probability[0][0] * 100:.2f}%")

    print(f"Survived     : {probability[0][1] * 100:.2f}%")

print("=" * 50)

# ----------------------------
# Data Scaling
# ----------------------------

scaler = StandardScaler()

scaled_data = scaler.fit_transform(input_data)

print("\nScaled Data")

print(scaled_data)