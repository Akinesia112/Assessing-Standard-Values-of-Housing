import pandas as pd

# Read the csv file and convert it to a DataFrame
file_path = r"D:\財稅\data\merged_file.csv"
df = pd.read_csv(file_path)

# Delete the duplicated floor addresses in 'X軸_transformed' and 'Y軸_transformed', keeping the first one
df = df.drop_duplicates(subset=['X軸_transformed', 'Y軸_transformed'])

# Drop the rows with missing values in the specified columns
columns_to_check = ['X軸', 'Y軸', '105公告現值', '108公告現值', '111公告現值', '113年公告現值', '105年評定之地段率', '108年評定之地段率', '111年評定之地段率']
df = df.dropna(subset=columns_to_check)

# Save the filtered DataFrame to a new CSV file
output_path = r"D:\財稅\data\filtered_file_dropMiss.csv"
df.to_csv(output_path, index=False)

print("檔案處理完成，已保存到", output_path)
