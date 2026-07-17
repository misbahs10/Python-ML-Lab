# 🌸 Iris Flower Classification using Machine Learning

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical-blue?style=for-the-badge&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-4C72B0?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

---

# 📌 Project Overview

The **Iris Flower Classification** project is a Machine Learning Classification project built using **Python** and **Scikit-learn**.

The objective of this project is to classify Iris flowers into one of the following species using flower measurements:

- 🌸 Setosa
- 🌸 Versicolor
- 🌸 Virginica

The model predicts the flower species based on:

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

This project demonstrates the complete Machine Learning workflow from **data preprocessing** to **model deployment-ready prediction**.

---

# 🎯 Project Objectives

- Load and preprocess the Iris dataset
- Perform Exploratory Data Analysis (EDA)
- Visualize the dataset using professional graphs
- Train multiple Machine Learning models
- Compare model performance
- Evaluate the trained model
- Save the best model
- Predict species from user input

---

# 🛠 Technologies Used

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

# 📂 Project Structure

```text
Iris-Flower-Classification/
│
├── data/
│   ├── iris.csv
│   └── iris-cleaned.csv
│
├── graphs/
│   ├── species_distribution.png
│   ├── pairplot.png
│   ├── heatmap.png
│   ├── feature_importance.png
│   ├── confusion_matrix.png
│   └── ...
│
├── models/
│   └── iris_model.pkl
│
├── notebooks/
│   └── Iris_EDA.ipynb
│
├── src/
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

# 📊 Dataset Information

Dataset Name:

**Iris Dataset**

Total Samples

```
150
```

Features

```
4
```

Target Classes

```
3
```

Feature Names

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

Target

```
Species
```

---

# 🌼 Iris Species

| Species | Description |
|----------|-------------|
| Setosa | Small petals with unique characteristics |
| Versicolor | Medium-sized petals |
| Virginica | Large petals |

---

# 📈 Exploratory Data Analysis

The notebook contains:

- Dataset Overview
- Dataset Information
- Missing Values
- Duplicate Values
- Statistical Summary
- Species Distribution
- Pairplot
- Correlation Heatmap
- Histograms
- Boxplots
- Violin Plots
- Scatter Plots
- Feature Importance
- Confusion Matrix
- Model Evaluation

---

# 📸 Visualizations

The notebook automatically saves all graphs inside the **graphs/** folder.

Generated Visualizations include:

- Species Distribution
- Pairplot
- Correlation Heatmap
- Histograms
- Boxplots
- Violin Plots
- Scatter Plot
- Feature Importance
- Confusion Matrix

---

# 🤖 Machine Learning Models

The following models were trained:

- Logistic Regression
- Random Forest Classifier

---

# 📊 Model Evaluation

Evaluation Metrics

- Accuracy Score
- Confusion Matrix
- Classification Report
- Cross Validation Score

Model Accuracy

```
96.67%
```

---

# 💻 Installation

Clone the repository

```bash
git clone https://github.com/misbahs10/Iris-Flower-Classification.git
```

Go to project directory

```bash
cd Iris-Flower-Classification
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Project

## Step 1

Data Preprocessing

```bash
python src/data_preprocessing.py
```

---

## Step 2

Model Training

```bash
python src/train_model.py
```

---

## Step 3

Prediction

```bash
python src/predict.py
```

---

# 🌸 Sample Prediction

Input

```text
Sepal Length : 5.1

Sepal Width : 3.5

Petal Length : 1.4

Petal Width : 0.2
```

Output

```text
Predicted Species : Setosa

Confidence Score : 100%
```

---

# 📁 Saved Model

The trained model is automatically saved as:

```text
models/iris_model.pkl
```

---

# 📊 Machine Learning Workflow

```text
Dataset
      │
      ▼
Data Preprocessing
      │
      ▼
Exploratory Data Analysis
      │
      ▼
Visualization
      │
      ▼
Train-Test Split
      │
      ▼
Model Training
      │
      ▼
Model Evaluation
      │
      ▼
Prediction
      │
      ▼
Model Saving
```

---

# 🚀 Future Improvements

- Hyperparameter Tuning
- GridSearchCV
- Streamlit Web Application
- Flask Deployment
- FastAPI REST API
- Docker Containerization
- Cloud Deployment
- CI/CD Integration

---

# 📚 Skills Demonstrated

- Data Cleaning
- Data Analysis
- Data Visualization
- Machine Learning
- Classification
- Feature Engineering
- Model Evaluation
- Cross Validation
- Model Serialization
- Python Programming
- Git & GitHub

---

# 💼 Resume Description

Developed an Iris Flower Classification model using Python and Scikit-learn to classify flower species based on sepal and petal measurements. Performed data preprocessing, exploratory data analysis, visualization, model training, evaluation, and prediction, achieving **96.67% classification accuracy**.

---

# 👩‍💻 Author

**Misbah Sajjad**

Python Developer | Machine Learning Enthusiast

GitHub:
https://github.com/misbahs10/Python-ML-Lab.git

LinkedIn:
https://linkedin.com/in/misbahsajjad23/

---

# ⭐ If you found this project helpful

Please consider giving this repository a ⭐ on GitHub.

---

# 📜 License

This project is licensed under the **MIT License**.