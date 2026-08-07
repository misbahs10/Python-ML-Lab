# 📊 Marketing Campaign Prediction using Machine Learning

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-green)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Project Overview

This project uses Machine Learning to predict whether a marketing campaign will be successful or rejected based on campaign-related features.

The goal of this project is to help businesses make data-driven marketing decisions by predicting campaign outcomes before investing resources.

---

## 🎯 Project Objectives

* Analyze marketing campaign data
* Perform data cleaning and preprocessing
* Explore important patterns using EDA
* Train Machine Learning classification models
* Evaluate model performance
* Build a prediction system
* Deploy an interactive Streamlit AI Dashboard

---

## 🛠️ Technologies Used

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Joblib
* Streamlit

### Tools

* Jupyter Notebook
* VS Code
* Git & GitHub

---

## 📂 Project Structure

```
Marketing-Campaign-Prediction/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── Marketing_Campaign_EDA.ipynb
│
├── src/
│   ├── config.py
│   ├── preprocessing.py
│   ├── train_model.py
│   └── predict.py
│
├── models/
│   └── campaign_model.pkl
│
├── outputs/
│   └── graphs/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🔍 Exploratory Data Analysis (EDA)

Performed analysis:

* Dataset information
* Missing value analysis
* Duplicate checking
* Feature distribution analysis
* Correlation analysis
* Target variable analysis
* Data visualization

---

# ⚙️ Machine Learning Workflow

The project follows these steps:

1. Data Collection
2. Data Cleaning
3. Feature Engineering
4. Data Preprocessing
5. Model Training
6. Model Evaluation
7. Prediction System Development
8. Streamlit Dashboard Deployment

---

# 🤖 Machine Learning Model

The classification model predicts:

* Campaign Accepted
* Campaign Rejected

Model saved using:

```
joblib
```

Saved model file:

```
campaign_model.pkl
```

---

# 📈 Model Evaluation

Evaluation metrics used:

* Accuracy Score
* Precision
* Recall
* F1 Score
* Confusion Matrix

---

# 🖥️ Streamlit AI Dashboard

An interactive dashboard was created where users can enter campaign details and get instant predictions.

Features:

* User-friendly interface
* Campaign prediction
* Success probability display
* Real-time results

Run dashboard:

```bash
streamlit run app.py
```

---

# Example Prediction

Example Output:

```
Prediction:
Campaign Accepted

Success Probability:
92%
```

---

# 📦 Installation & Setup

Clone repository:

```bash
git clone https://github.com/misbahs10/Marketing-Campaign-Prediction.git
```

Move into project folder:

```bash
cd Marketing-Campaign-Prediction
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run app.py
```

---

# 💡 Key Learnings

Through this project, I learned:

* Complete Machine Learning project workflow
* Data preprocessing techniques
* Classification algorithms
* Model deployment using Streamlit
* Creating production-style project structure
* GitHub project management

---

# 👩‍💻 Author

**Misbah Sajjad**

AI & Data Science Enthusiast

Skills:

* Python
* Machine Learning
* Data Analytics
* Power BI
* SQL
* AI Automation

---

If you like this project, consider giving it a star!
