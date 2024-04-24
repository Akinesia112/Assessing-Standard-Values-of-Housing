import geopandas as gpd

# Read the original GeoJSON file into a GeoDataFrame
# gdf = gpd.read_file(r"D:\財稅\data\raw\meta_data\meta_data_updated.geojson")
gdf = gpd.read_file(r"D:\財稅\data\raw\meta_data\meta_data_updated_output_only_Tainan.geojson")

# Define the columns to keep
'''
columns_to_keep = [
    "id",
     "105APV_weighted_avg", "105RAR_point_count", "105RAR_weighted_avg",
    "108APV_point_count", "108APV_weighted_avg", "108RAR_point_count", "108RAR_weighted_avg",
    "111APV_point_count", "111APV_weighted_avg", "111RAR_point_count", "111RAR_weighted_avg",
    "113APV_point_count", "113APV_weighted_avg", 
    "geometry"  # Always keep the geometry column
]
'''
columns_to_keep = [
    "id",
     "105APV_weighted_avg", "105RAR_weighted_avg",
    "108APV_weighted_avg", "108RAR_weighted_avg",
    "111APV_weighted_avg", "111RAR_weighted_avg",
    "113APV_weighted_avg", 
    "geometry",  # Always keep the geometry column
    "預測值"
]

# Select only the desired columns
gdf_selected = gdf[columns_to_keep]

# Write the selected data to a new GeoJSON file
# output_path = r"D:\財稅\data\raw\meta_data\meta_data_web_test_avg_only_Tainan.geojson"
output_path = r"D:\財稅\data\raw\meta_data\meta_data_updated_output_only_Tainan.geojson"

gdf_selected.to_file(output_path, driver='GeoJSON', encoding='utf-8-sig')

# gdf_selected.to_csv(r"D:\財稅\data\raw\meta_data\meta_data_web_test_avg_only_Tainan.csv", index=False, encoding='utf-8-sig')
gdf_selected.to_csv(r"D:\財稅\data\raw\meta_data\meta_data_updated_output_only_Tainan.csv", index=False, encoding='utf-8-sig')

print(f"Selected columns have been saved to {output_path}")
