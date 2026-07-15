# ============================================
# Student Performance Prediction
# Prediction
# ============================================

import joblib # type: ignore
import pandas as pd # type: ignore

# ============================================
# Load Model & Encoders
# ============================================

model = joblib.load("models/student_model.pkl")
encoders = joblib.load("models/encoders.pkl")

print("=" * 60)
print("Student Performance Prediction")
print("=" * 60)

# ============================================
# User Input
# ============================================

hours_studied = float(input("Hours Studied: "))
attendance = float(input("Attendance (%): "))

parental_involvement = input("Parental Involvement (Low/Medium/High): ")
access_to_resources = input("Access to Resources (Low/Medium/High): ")
extracurricular = input("Extracurricular Activities (Yes/No): ")

sleep_hours = float(input("Sleep Hours: "))
previous_scores = float(input("Previous Scores: "))

motivation = input("Motivation Level (Low/Medium/High): ")
internet = input("Internet Access (Yes/No): ")

tutoring = int(input("Tutoring Sessions: "))

family_income = input("Family Income (Low/Medium/High): ")
teacher_quality = input("Teacher Quality (Low/Medium/High): ")
school_type = input("School Type (Public/Private): ")
peer = input("Peer Influence (Negative/Neutral/Positive): ")

physical_activity = float(input("Physical Activity (Hours): "))

learning = input("Learning Disabilities (Yes/No): ")

parent_education = input(
    "Parental Education (High School/College/Postgraduate): "
)

distance = input(
    "Distance From Home (Near/Moderate/Far): "
)

gender = input("Gender (Male/Female): ")

# ============================================
# Create DataFrame
# ============================================

input_data = pd.DataFrame({

    "Hours_Studied":[hours_studied],
    "Attendance":[attendance],
    "Parental_Involvement":[parental_involvement],
    "Access_to_Resources":[access_to_resources],
    "Extracurricular_Activities":[extracurricular],
    "Sleep_Hours":[sleep_hours],
    "Previous_Scores":[previous_scores],
    "Motivation_Level":[motivation],
    "Internet_Access":[internet],
    "Tutoring_Sessions":[tutoring],
    "Family_Income":[family_income],
    "Teacher_Quality":[teacher_quality],
    "School_Type":[school_type],
    "Peer_Influence":[peer],
    "Physical_Activity":[physical_activity],
    "Learning_Disabilities":[learning],
    "Parental_Education_Level":[parent_education],
    "Distance_from_Home":[distance],
    "Gender":[gender]

})

# ============================================
# Encode Categorical Columns
# ============================================

for column, encoder in encoders.items():

    if column in input_data.columns:

        input_data[column] = encoder.transform(input_data[column])

# ============================================
# Prediction
# ============================================

prediction = model.predict(input_data)

# Decode Performance

performance_encoder = encoders["Performance"]

result = performance_encoder.inverse_transform(prediction)

print("\n" + "=" * 60)
print("Predicted Student Performance")
print("=" * 60)

print(f"\nResult : {result[0]}")

print("=" * 60)