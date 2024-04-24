import pandas as pd

# Read the two CSV files
file1_df = pd.read_csv('D:/財稅/data/臺南市37行政區稅籍資料_transformed.csv')
file2_df = pd.read_csv('D:/財稅/data/1130301-公告現值.csv', encoding='utf-8')

# Merge the two dataframes on the '稅號' column
merged_df = pd.merge(file1_df, file2_df, on='稅號')

# Save the merged dataframe to a new CSV file
merged_df.to_csv('D:/財稅/data/merged_file.csv', index=False, encoding='utf-8-sig')

# Print head 5 rows of the merged dataframe
print(merged_df.head())
