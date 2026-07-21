# 🥇 HR Employee Attrition Prediction

A professional Machine Learning classification project that predicts whether an employee is likely to leave the company using the IBM HR Analytics Employee Attrition dataset.

---

# 📌 Project Overview

Employee attrition is one of the biggest challenges for organizations.

This project uses Machine Learning to identify employees who are likely to leave the company based on demographic, work-related, and performance-related features.

The project follows a complete Machine Learning workflow including:

- Data Preprocessing
- Exploratory Data Analysis
- Feature Engineering
- Model Training
- Model Evaluation
- Prediction System

---

# 🚀 Project Features

- Professional Folder Structure
- Clean & Modular Python Code
- Data Preprocessing Pipeline
- Exploratory Data Analysis (EDA)
- Beautiful Visualizations
- Multiple Machine Learning Models
- Automatic Best Model Selection
- Saved Machine Learning Model
- Prediction Script
- Professional GitHub Ready Project

---

# 📂 Project Structure

```text
HR-Employee-Attrition-Prediction
│
├── data/
│
├── models/
│   ├── employee_attrition_model.pkl
│   ├── scaler.pkl
│   └── feature_columns.pkl
│
├── notebooks/
│   └── Employee_Attrition_EDA.ipynb
│
├── reports/
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   ├── feature_importance.png
│   ├── model_comparison.png
│   └── EDA graphs
│
├── src/
│   ├── config.py
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── predict.py
│   └── utils.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# 📊 Dataset

IBM HR Analytics Employee Attrition & Performance Dataset

Dataset contains employee information such as

- Age
- Gender
- Department
- Job Role
- Monthly Income
- Job Satisfaction
- Overtime
- Total Working Years
- Years at Company
- Performance Rating

Target Variable

```
Attrition

No

Yes
```

---

# ⚙️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Joblib
- Jupyter Notebook

---

# 🤖 Machine Learning Models

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier

---

# 📈 Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC Score
- Confusion Matrix

---

# 📷 Generated Visualizations

The project automatically generates and saves:

- Attrition Distribution
- Gender Distribution
- Department Distribution
- Age Distribution
- Monthly Income Distribution
- Job Satisfaction Analysis
- Overtime vs Attrition
- Correlation Heatmap
- Feature Importance
- ROC Curve
- Confusion Matrix
- Model Comparison

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/misbahs10/HR-Employee-Attrition-Prediction.git
```

Go to project folder

```bash
cd HR-Employee-Attrition-Prediction
```

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Project

### Data Preprocessing

```bash
python src/data_preprocessing.py
```

### Model Training

```bash
python src/train_model.py
```

### Prediction

```bash
python src/predict.py
```

---

# 📈 Results

The model successfully predicts whether an employee is likely to leave the company using historical HR data.

The project compares multiple Machine Learning algorithms and automatically saves the trained model for future predictions.

---

# 💼 Resume Description

Developed a Machine Learning classification model to predict employee attrition using IBM HR Analytics data. Implemented data preprocessing, exploratory data analysis, feature engineering, multiple classification models, and performance evaluation to identify factors contributing to workforce turnover.

---

# 🔮 Future Improvements

- Hyperparameter Tuning
- Cross Validation
- SMOTE for Class Imbalance
- XGBoost Classifier
- LightGBM
- CatBoost
- Streamlit Web Application
- Flask API Deployment

---

# 👨‍💻 Author

**Misbah Sajjad**

Machine Learning | Data Science | Python Developer

---

# 📜 License

This project is licensed under the MIT License.