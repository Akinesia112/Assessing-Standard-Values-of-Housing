import os
import geopandas as gpd
import pandas as pd

# Define input and output directory paths
input_directory = r"D:\財稅\data\raw\GoogleMaps_Grid_Mapping" # 2024 Google Map POIs files directory

merged_data = r"D:\財稅\data\raw\merged_data.csv" # merge data from tax and landuse files

output_csv_path = r"D:\財稅\data\raw\merged_data_all.csv"

# Get a list of all GeoJSON files in the directory
geojson_files = [f for f in os.listdir(input_directory) if f.endswith('.geojson')]

# Initialize an empty DataFrame to store all merged data
merged_df = pd.DataFrame()

# Process each GeoJSON file
for file in geojson_files:
    file_path = os.path.join(input_directory, file)
    gdf = gpd.read_file(file_path)

    # Print file processing status
    print(f"Processing {file} with columns: {gdf.columns.tolist()}")

    # Handling specific files with unique requirements
    if file == 'Grid_more_data.geojson':
        poi_columns = ['id', '交通_公車站', '交通_火車站', '交通_腳踏車站', '公設_公園', '公設_郵局', 
                       '嫌惡設施_危險', '嫌惡設施_殯葬', '嫌惡設施_髒亂', '教育_國中', '教育_國小', 
                       '教育_大學', '教育_補習班', '教育_高中', '醫療_診所', '醫療_醫院', '餐飲_食物']
        gdf = gdf[poi_columns]
    else:
        if 'point_count' in gdf.columns:
            column_prefix = file.split("Grid_output_")[-1].replace('.geojson', '')
            gdf.rename(columns={'point_count': f'{column_prefix}_point_count'}, inplace=True)

        # Keep only id and point_count columns
        gdf = gdf[['id'] + [col for col in gdf.columns if col.endswith('_point_count')]]

    # Perform the merge operation
    if merged_df.empty:
        merged_df = gdf
    else:
        merged_df = pd.merge(merged_df, gdf, on='id', how='outer')

        # Drop the duplicated columns post-merge
        cols_to_drop = ['index_right_x', 'bottom_x', 'top_x', 'left_x', 'WKT_x', 
                        'index_right_y', 'bottom_y', 'top_y', 'left_y', 'WKT_y']
        merged_df.drop(columns=[col for col in cols_to_drop if col in merged_df.columns], inplace=True)

# Load the existing merged data
merged_data_df = pd.read_csv(merged_data)
merged_data_df['id'] = merged_data_df['id'].astype(str)

# Merge the cumulative data with the additional geo data
final_df = pd.merge(merged_df, merged_data_df, on='id', how='outer')

# Save the final merged DataFrame to a CSV file
final_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
print("All data merged and saved.")
