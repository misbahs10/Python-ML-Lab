# 🎓 Student Performance Prediction

A Machine Learning Classification Project that predicts a student's academic performance based on study habits, attendance, previous scores, and other academic factors.

---

## 📌 Project Overview

The goal of this project is to analyze student-related factors and predict whether a student's performance will be:

- 🔴 Poor
- 🟡 Average
- 🟢 Excellent

This project demonstrates the complete Machine Learning workflow, including data preprocessing, exploratory data analysis (EDA), feature engineering, model training, evaluation, and prediction.

---

## 📂 Project Structure

```text
Student-Performance-Prediction/
│
├── data/
|   ├── student_cleaned.csv
│   └── student_data.csv
│
├── models/
│   ├── student_model.pkl
│   └── encoders.pkl
│
├── notebooks/
│   └── Student_EDA.ipynb
│
├── src/
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── predict.py
│   └── utils.py
│
├── images/
│   ├── all_histograms.png
│   ├── correlation_heatmap.png
│   ├── exam_score_distribution.png
│   ├── hours_studied_vs_exam_score.png
│   ├── attendance_vs_exam_score.png
│   ├── previous_scores_vs_exam_score.png
│   ├── hours_studied_boxplot.png
│   ├── gender_distribution.png
│   ├── school_type_distribution.png
│   ├── internet_access_distribution.png
│   ├── pairplot.png
│   └── performance_distribution.png
│
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
└── main.py
```

---

## 📊 Dataset Features

The dataset contains the following features:

- Hours_Studied
- Attendance
- Parental_Involvement
- Access_to_Resources
- Extracurricular_Activities
- Sleep_Hours
- Previous_Scores
- Motivation_Level
- Internet_Access
- Tutoring_Sessions
- Family_Income
- Teacher_Quality
- School_Type
- Peer_Influence
- Physical_Activity
- Learning_Disabilities
- Parental_Education_Level
- Distance_from_Home
- Gender

### 🎯 Target Variable

- Performance
  - Poor
  - Average
  - Excellent

---

## ⚙️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Joblib
- Jupyter Notebook
- VS Code

---

## 🚀 Machine Learning Workflow

1. Data Collection
2. Data Cleaning
3. Missing Value Handling
4. Exploratory Data Analysis (EDA)
5. Feature Engineering
6. Label Encoding
7. Train-Test Split
8. Model Training
9. Model Evaluation
10. Prediction

---

## 🤖 Machine Learning Models

The following classification algorithms were used:

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier

The best-performing model is automatically saved.

---

## 📈 Evaluation Metrics

The models were evaluated using:

- Accuracy
- Classification Report
- Precision
- Recall
- F1 Score
- Confusion Matrix

---

## ▶️ How to Run the Project

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/Student-Performance-Prediction.git
```

---

### 2. Move to Project Folder

```bash
cd Student-Performance-Prediction
```

---

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

---

### 4. Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

---

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 6. Train the Model

```bash
python src/train_model.py
```

---

### 7. Predict Student Performance

```bash
python src/predict.py
```

---

## 📷 Example Prediction

Input

```text
Hours Studied : 8

Attendance : 90

Previous Score : 85

Sleep Hours : 7

Motivation Level : High
```

Output

```text
Excellent
```

---

## 📌 Project Features

✔ Data Cleaning

✔ Missing Value Handling

✔ Exploratory Data Analysis

✔ Feature Engineering

✔ Classification Models

✔ Model Evaluation

✔ Prediction System

✔ Model Serialization

✔ Professional Project Structure

---

## 📚 Learning Outcomes

Through this project, I learned:

- Data preprocessing
- Data visualization
- Feature engineering
- Classification algorithms
- Model evaluation
- Model serialization using Joblib
- Real-world Machine Learning workflow

---

## 👩‍💻 Author

**Misbah Sajjad**

Python & Machine Learning Learner

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourusername

---

## ⭐ If you found this project helpful, please consider giving it a Star.