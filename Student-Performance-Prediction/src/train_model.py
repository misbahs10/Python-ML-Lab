# ============================================
# Student Performance Prediction
# Model Training (Classification)
# ============================================

import pandas as pd # type: ignore
import joblib # type: ignore

from sklearn.model_selection import train_test_split # type: ignore
from sklearn.preprocessing import LabelEncoder # type: ignore

from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.tree import DecisionTreeClassifier # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore

from sklearn.metrics import ( # type: ignore
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ============================================
# Load Dataset
# ============================================

data = pd.read_csv("data/student_data.csv")

# ============================================
# Handle Missing Values
# ============================================

numeric_columns = data.select_dtypes(include=["number"]).columns

for col in numeric_columns:
    data[col] = data[col].fillna(data[col].median())

categorical_columns = data.select_dtypes(include=["object", "string"]).columns

for col in categorical_columns:
    data[col] = data[col].fillna(data[col].mode()[0])

# ============================================
# Create Target Column
# ============================================

def performance(score):

    if score < 60:
        return "Poor"

    elif score < 80:
        return "Average"

    else:
        return "Excellent"


data["Performance"] = data["Exam_Score"].apply(performance)

data.drop("Exam_Score", axis=1, inplace=True)

# ============================================
# Encode Categorical Columns
# ============================================

encoders = {}

categorical_columns = data.select_dtypes(include=["object", "string"]).columns

for col in categorical_columns:

    encoder = LabelEncoder()

    data[col] = encoder.fit_transform(data[col])

    encoders[col] = encoder

# ============================================
# Save Encoders
# ============================================

joblib.dump(encoders, "models/encoders.pkl")

print("Encoders Saved Successfully")

# ============================================
# Features & Target
# ============================================

X = data.drop("Performance", axis=1)

y = data["Performance"]

# ============================================
# Train Test Split
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ============================================
# Models
# ============================================

models = {

    "Logistic Regression":
    LogisticRegression(max_iter=5000),

    "Decision Tree":
    DecisionTreeClassifier(random_state=42),

    "Random Forest":
    RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

}

best_model = None
best_accuracy = 0

# ============================================
# Train Models
# ============================================

for name, model in models.items():

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)

    print(f"\nAccuracy : {accuracy:.4f}")

    print("\nClassification Report")
    print(classification_report(y_test, prediction))

    print("\nConfusion Matrix")
    print(confusion_matrix(y_test, prediction))

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model

# ============================================
# Save Best Model
# ============================================

joblib.dump(best_model, "models/student_model.pkl")

print("\n" + "=" * 60)
print("Best Model Saved Successfully")
print(f"Best Accuracy : {best_accuracy:.4f}")
print("=" * 60)