"""
===========================================
House Price Prediction
Data Visualization
===========================================
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import DATA_PATH, IMAGE_DIR


# Create images folder
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load dataset
data = pd.read_csv(DATA_PATH)

# ----------------------------
# Histogram
# ----------------------------
plt.figure(figsize=(8, 5))
plt.hist(data["price"], bins=20)
plt.title("House Price Distribution")
plt.xlabel("Price")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "price_distribution.png"))
plt.close()

# ----------------------------
# Correlation Heatmap
# ----------------------------
plt.figure(figsize=(8, 6))
sns.heatmap(data.select_dtypes(include="number").corr(),
            annot=True,
            cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "correlation_heatmap.png"))
plt.close()

# ----------------------------
# Bedrooms Count
# ----------------------------
plt.figure(figsize=(6, 4))
sns.countplot(x="bedrooms", data=data)
plt.title("Bedrooms Count")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "bedrooms_count.png"))
plt.close()

# ----------------------------
# Area vs Price
# ----------------------------
plt.figure(figsize=(8, 5))
sns.scatterplot(x="area", y="price", data=data)
plt.title("Area vs Price")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "area_vs_price.png"))
plt.close()

print("\n✅ All graphs saved successfully inside images folder.")