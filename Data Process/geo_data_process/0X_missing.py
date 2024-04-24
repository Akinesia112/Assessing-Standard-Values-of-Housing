import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.font_manager import FontProperties

# Load the data
file_path = "D:/財稅/data/filtered_file_dropMiss.csv"

data = pd.read_csv(file_path)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Use Microsoft YaHei font
plt.rcParams['axes.unicode_minus'] = False  # Solve the problem that the negative sign is displayed as a square when using Microsoft YaHei

# Check for missing values in each column
missing_values_count = data.isnull().sum()

# Print the number of missing values for each column
print("Number of missing values in each column:")
print(missing_values_count)

# Calculate the percentage of missing values for each column
total_cells = np.product(data.shape)
total_missing = missing_values_count.sum()
print(f"Percentage of data that is missing: {(total_missing/total_cells) * 100}%")

# Visualization of missing data
plt.figure(figsize=(12, 12))
sns.heatmap(data.isnull(), cbar=False, cmap='BuPu')
plt.title('Heatmap of Missing Values in Data')
plt.show()

# Calculate and print the percentage of missing values for each variable
missing_percentage = (data.isnull().sum() / len(data)) * 100
print("Percentage of missing values for each column:")
print(missing_percentage)
