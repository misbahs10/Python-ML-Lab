import joblib # type: ignore
import pandas as pd # type: ignore

from config import (
    MODEL_PATH,
    SCALER_PATH,
    FEATURE_COLUMNS_PATH,
)

print("=" * 60)
print("HR EMPLOYEE ATTRITION PREDICTION")
print("=" * 60)

# Load Model
model = joblib.load(MODEL_PATH)

# Load Scaler
scaler = joblib.load(SCALER_PATH)

# Load Feature Columns
feature_columns = joblib.load(FEATURE_COLUMNS_PATH)

# Empty DataFrame
input_df = pd.DataFrame(
    [[0] * len(feature_columns)],
    columns=feature_columns
)

print("\nEnter Employee Details\n")

# ===============================
# Numerical Features
# ===============================

age = int(input("Age : "))
distance = int(input("Distance From Home : "))
income = int(input("Monthly Income : "))
companies = int(input("Number of Companies Worked : "))
working_years = int(input("Total Working Years : "))
years_company = int(input("Years At Company : "))
years_role = int(input("Years In Current Role : "))
years_manager = int(input("Years With Current Manager : "))

# Fill numerical columns
input_df["Age"] = age
input_df["DistanceFromHome"] = distance
input_df["MonthlyIncome"] = income
input_df["NumCompaniesWorked"] = companies
input_df["TotalWorkingYears"] = working_years
input_df["YearsAtCompany"] = years_company
input_df["YearsInCurrentRole"] = years_role
input_df["YearsWithCurrManager"] = years_manager

# ===============================
# Overtime
# ===============================

overtime = input("OverTime (Yes/No): ").strip().title()

column = f"OverTime_{overtime}"

if column in input_df.columns:
    input_df[column] = 1

# ===============================
# Gender
# ===============================

gender = input("Gender (Male/Female): ").strip().title()

column = f"Gender_{gender}"

if column in input_df.columns:
    input_df[column] = 1

# ===============================
# Scale
# ===============================

scaled = scaler.transform(input_df)

# Prediction

prediction = model.predict(scaled)[0]

probability = model.predict_proba(scaled)[0][1]

print("\n" + "=" * 60)

if prediction == 1:

    print("Prediction : Employee Will Leave")

else:

    print("Prediction : Employee Will Stay")

print(f"Probability : {probability*100:.2f}%")

print("=" * 60)