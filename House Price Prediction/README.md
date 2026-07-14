# House Price Prediction using Machine Learning

## Overview

### House Price Prediction using Machine Learning

Built a machine learning regression model to predict house prices using Python, Pandas, NumPy, and Scikit-learn. Performed data preprocessing, feature engineering, model training, evaluation, visualization, and developed a command-line prediction system.

---

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Machine Learning
- Linear Regression
- Decision Tree
- Random Forest
- Data Preprocessing
- Data Visualization
- Model Evaluation
- Joblib

---

## Dataset Features

- Area
- Bedrooms
- Bathrooms
- Stories
- Main Road
- Guest Room
- Basement
- Hot Water Heating
- Air Conditioning
- Parking
- Preferred Area
- Furnishing Status

Target:

Price

---

## Machine Learning Models

- Linear Regression ✅
- Decision Tree Regressor
- Random Forest Regressor

---

## Best Model

Linear Regression

R² Score = 0.6529

---

## Installation

pip install -r requirements.txt

---

## Train Model

python src/train_model.py

---

## Predict

python src/predict.py

---

## Visualize Dataset

python src/visualization.py

---

## Project Structure

House Price Prediction/
│
├── dataset/
│   └── Housing.csv
│
├── images/
│   ├── area_vs_price.png
│   ├── bedrooms_count.png
│   ├── correlation_heatmap.png
│   └── price_distribution.png
│
├── models/
│   └── house_price_model.pkl
│
├── notebooks/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── utils.py
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── evaluate.py
│   ├── predict.py
│   └── visualization.py
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE