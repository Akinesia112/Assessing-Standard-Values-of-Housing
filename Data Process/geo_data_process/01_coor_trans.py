import pandas as pd
from pyproj import Proj, Transformer

# Note: The file path and encoding might need to be adjusted for execution in a different environment
file_path = "D:/財稅/data/臺南市37行政區稅籍資料.csv"
data = pd.read_csv(file_path, encoding='big5')

# Define the coordinate systems for the transformation using Transformer
transformer = Transformer.from_crs("epsg:3826", "epsg:4326", always_xy=True)

# Apply the transformation to the "X軸" and "Y軸" columns
data[['X軸_transformed', 'Y軸_transformed']] = data.apply(lambda row: transformer.transform(row['X軸'], row['Y軸']), axis=1, result_type="expand")

# Now, 'data' contains the original X軸, Y軸 columns as well as the transformed 'X軸_transformed', 'Y軸_transformed' columns
print(data[['X軸', 'Y軸', 'X軸_transformed', 'Y軸_transformed']].head())

# Save the transformed data to a new CSV file
output_file_path = "D:/財稅/data/臺南市37行政區稅籍資料_transformed.csv"
data.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"Data saved to {output_file_path}")
