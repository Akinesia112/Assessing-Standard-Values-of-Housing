import os
import geopandas as gpd
import pandas as pd

# Define input and output directory paths
input_directory = r"D:\財稅\data\raw\Grid" # Tax files directory

output_csv_path = r"D:\財稅\data\raw\merged_data.csv"
land_use_path = r"D:\財稅\data\raw\output_final0227.csv" 

# Get a list of all GeoJSON files in the directory
geojson_files = [f for f in os.listdir(input_directory) if f.endswith('.geojson')]

# Initialize an empty DataFrame to store all merged data
merged_df = pd.DataFrame()

# Process each GeoJSON file
for file in geojson_files:
    file_path = os.path.join(input_directory, file)
    gdf = gpd.read_file(file_path)
    
    # Extract the prefix from the filename to use in renaming columns
    column_prefix = file.split('_Grid_Count_and_Weighted')[0]
    
    # Select and rename fields
    if 'weighted_avg' in gdf.columns:
        gdf.rename(columns={'weighted_avg': f'{column_prefix}_weighted_avg'}, inplace=True)
    if 'point_count' in gdf.columns:
        gdf.rename(columns={'point_count': f'{column_prefix}_point_count'}, inplace=True)
    if 'weighted_volumerate_avg' in gdf.columns:
        gdf.rename(columns={'weighted_volumerate_avg': f'{column_prefix}_weighted_volumerate_avg'}, inplace=True)
    if 'weighted_buildrate_avg' in gdf.columns:
        gdf.rename(columns={'weighted_buildrate_avg': f'{column_prefix}_weighted_buildrate_avg'}, inplace=True)

    # Convert keys to strings to ensure consistent types for merging
    merge_keys = ['id', 'WKT', 'left', 'top', 'bottom', 'index_right']
    for key in merge_keys:
        gdf[key] = gdf[key].astype(str)
        
    # Check for duplicates in the current DataFrame before merging
    if gdf.duplicated(subset='id').any():
        print(f"Duplicate IDs found in {file}")
    
    # Add selected columns to the DataFrame
    columns_to_keep = merge_keys + [col for col in gdf.columns if col.endswith('_avg') or col.endswith('_point_count')]
    gdf = gdf[columns_to_keep]
    
    # Merge the current DataFrame with the cumulative DataFrame
    if merged_df.empty:
        merged_df = gdf
    else:
        # Merge and keep only the first of duplicate rows based on 'id'
        merged_df = pd.merge(merged_df.drop_duplicates(subset='id'), gdf.drop_duplicates(subset='id'), on=merge_keys, how='outer')
    
    print(f"Merged {file}")
    

# Load the land use data
land_use_df = pd.read_csv(land_use_path)
land_use_df['id'] = land_use_df['id'].astype(str)  # Ensure the 'id' column is string type

# Merge the land use data with the cumulative geo data
final_df = pd.merge(merged_df, land_use_df, on='id', how='outer')

# Save the final merged DataFrame to a CSV file
final_df.to_csv(output_csv_path, index=False)
print("All data merged and saved.")