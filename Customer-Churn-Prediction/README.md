# 🚀 Customer Churn Prediction

A complete end-to-end Machine Learning project that predicts whether a customer is likely to leave a company (Customer Churn Prediction). The project covers data preprocessing, exploratory data analysis (EDA), feature engineering, model training, evaluation, visualization, and prediction using multiple classification algorithms.

---

# 📌 Project Overview

Customer churn is one of the most important business problems in industries such as Telecom, Banking, SaaS, and Subscription-based services.

This project builds a machine learning model to predict customer churn by analyzing customer demographics, service usage, contract details, and billing information.

The project follows an end-to-end machine learning workflow from raw data to deployment-ready prediction.

---

# 📂 Project Structure

```text
Customer-Churn-Prediction/
│
├── data/
│   ├── raw/
│   │   └── Customer_Churn.csv
│   │
│   └── processed/
│       └── customer_churn_clean.csv
│
├── models/
│   ├── churn_model.pkl
│   └── feature_columns.pkl
│
├── outputs/
│   ├── graphs/
│   │   ├── churn_distribution.png
│   │   ├── correlation_heatmap.png
│   │   ├── confusion_matrix.png
│   │   ├── roc_curve.png
│   │   ├── feature_importance.png
│   │   ├── contract_vs_churn.png
│   │   ├── internet_service_vs_churn.png
│   │   ├── tenure_distribution.png
│   │   ├── monthly_charges_distribution.png
│   │   ├── boxplot_monthlycharges.png
│   │   └── pairplot.png
│   │
│   └── reports/
│       └── model_report.txt
│
├── notebooks/
│   └── Customer_Churn_EDA.ipynb
│
├── src/
│   ├── config.py
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── predict.py
│   ├── visualization.py
│   └── utils.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📊 Dataset

**Dataset Name:** Customer Churn Dataset

### Features

* Gender
* Senior Citizen
* Partner
* Dependents
* Tenure
* Phone Service
* Multiple Lines
* Internet Service
* Online Security
* Online Backup
* Device Protection
* Tech Support
* Streaming TV
* Streaming Movies
* Contract
* Paperless Billing
* Payment Method
* Monthly Charges
* Total Charges

### Target Variable

**Churn**

* Yes
* No

---

# ⚙️ Project Workflow

1. Data Loading
2. Data Cleaning
3. Missing Value Handling
4. Duplicate Removal
5. Feature Encoding
6. Exploratory Data Analysis (EDA)
7. Feature Engineering
8. Train-Test Split
9. Model Training
10. Model Evaluation
11. Best Model Selection
12. Prediction
13. Report Generation
14. Visualization

---

# 🤖 Machine Learning Models

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier

The project automatically selects the best-performing model based on evaluation metrics.

---

# 📈 Model Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC Score
* Classification Report
* Confusion Matrix

---

# 📊 Visualizations

The project automatically generates professional visualizations.

* Customer Churn Distribution
* Monthly Charges Distribution
* Tenure Distribution
* Boxplot
* Contract vs Churn
* Internet Service vs Churn
* Correlation Heatmap
* Confusion Matrix
* ROC Curve
* Feature Importance
* Pairplot

All graphs are automatically saved inside the **outputs/graphs/** folder.

---

# 🛠 Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Joblib
* Jupyter Notebook

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/misbahs10/Customer-Churn-Prediction.git
```

Move into the project folder:

```bash
cd Customer-Churn-Prediction
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Project

### Step 1

```bash
python src/data_preprocessing.py
```

### Step 2

```bash
python src/train_model.py
```

### Step 3

```bash
python src/predict.py
```

---

# 📁 Output Files

After training, the following files are automatically generated:

## Models

* churn_model.pkl
* feature_columns.pkl

## Reports

* model_report.txt

## Graphs

* Correlation Heatmap
* Confusion Matrix
* ROC Curve
* Feature Importance
* Pairplot
* Churn Distribution
* Contract vs Churn
* Internet Service vs Churn
* Monthly Charges Distribution
* Tenure Distribution
* Boxplot

---

# 🎯 Project Features

* End-to-End Machine Learning Project
* Clean Project Structure
* Automatic Data Preprocessing
* Feature Engineering
* Multiple Classification Algorithms
* Automatic Best Model Selection
* Professional Visualizations
* Model Saving
* Prediction Script
* Report Generation
* GitHub Ready
* ATS Resume Ready

---

# 📈 Accuracy

The project evaluates multiple machine learning models and automatically selects the best-performing model based on evaluation metrics.

Typical evaluation metrics include:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC Score

The final accuracy depends on the dataset and the selected model.

---

# 🚀 Future Improvements

* Hyperparameter Tuning (GridSearchCV / RandomizedSearchCV)
* Cross Validation
* XGBoost Classifier
* LightGBM Classifier
* CatBoost Classifier
* SHAP Explainability
* Streamlit Web Application
* Docker Deployment
* REST API using FastAPI
* Cloud Deployment

---

# 💼 Resume Description

**Customer Churn Prediction | Python, Pandas, NumPy, Scikit-learn**

Developed an end-to-end machine learning solution to predict customer churn using Logistic Regression, Decision Tree, and Random Forest classifiers. Performed data preprocessing, feature engineering, exploratory data analysis, model evaluation, and automated best-model selection. Generated professional visualizations, saved trained models, and built a prediction pipeline for customer retention analysis.

---

# 👨‍💻 Author

**Misbah Sajjad**

AI & Data Science Enthusiast

Python | Machine Learning | Data Analysis | Power BI | SQL

---

⭐ If you found this project useful, consider giving it a star on GitHub!
