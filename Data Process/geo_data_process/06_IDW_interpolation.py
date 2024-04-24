import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point
import os

# Define the input and output directories
input_directory = r"D:\財稅\data\raw"
output_directory = r"D:\財稅\data\raw\interpolated"

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    
# List all geojson files in the input directory
def list_geojson_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.geojson')]


# IDW Interpolated Function
def idw_interpolation(gdf, value_field, k):
    gdf['center'] = gdf.geometry.centroid
    coords = np.array(list(gdf['center'].apply(lambda geom: (geom.x, geom.y))))
    
    # Filter for rows where the value_field is not zero and build the KDTree on their coordinates
    mask_non_zero = gdf[value_field] != 0
    non_zero_coords = coords[mask_non_zero]
    non_zero_values = gdf.loc[mask_non_zero, value_field]
    if len(non_zero_coords) == 0:
        print(f"No non-zero values found for field '{value_field}'. Skipping interpolation.")
        return
    
    tree = cKDTree(non_zero_coords)
    
    # Interpolate for rows where the value_field is zero
    for index, row in gdf[gdf[value_field] == 0].iterrows():
        point_coords = np.array([row['center'].x, row['center'].y])
        dists, idx = tree.query(point_coords, k=min(k, len(non_zero_coords)))
        dists = np.where(dists == 0, 1e-10, dists)  # Avoid division by zero
        weights = 1 / dists
        idw_value = np.sum(weights * non_zero_values.iloc[idx]) / np.sum(weights)
        gdf.at[index, value_field] = idw_value
        
        print("Interpolated value for grid", index, "is", idw_value)

# The fields to check for interpolation
fields_to_interpolate = ['weighted_volumerate_avg', 'weighted_buildrate_avg', "weighted_avg"]

# Process each .geojson file
for filename in list_geojson_files(input_directory):
    file_path = os.path.join(input_directory, filename)
    gdf = gpd.read_file(file_path, encoding='utf-8-sig')
    
    print("================================================================================")
    print(f"Processing {file_path}")
    print("================================================================================")

    # Set CRS and convert if needed
    if gdf.crs is None:
        gdf.set_crs('EPSG:3857', inplace=True)
    gdf = gdf.to_crs(3857)

    # Perform IDW interpolation for the specified fields if they exist
    for field in fields_to_interpolate:
        if field in gdf.columns:
            idw_interpolation(gdf, field, 24)
            print("Interpolated", field, "values for", filename)

    # Remove the 'center' column if it exists
    if 'center' in gdf.columns:
        gdf.drop('center', axis=1, inplace=True)

    # Reset index to ensure a clean dataframe
    gdf.reset_index(drop=True, inplace=True)

    # Set the geometry column and CRS again to avoid any issues
    gdf.set_geometry('geometry', inplace=True)
    gdf.set_crs('EPSG:3857', inplace=True)

    # Construct the output file path
    output_file_path = os.path.join(output_directory, filename.replace('.geojson', '_interpolated.geojson'))

    # Attempt to save the GeoDataFrame to a GeoJSON file
    try:
        gdf.to_file(output_file_path, driver='GeoJSON', encoding='utf-8-sig')
        print(f"File saved successfully to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while saving {output_file_path}: {e}")



# The fields to check for interpolation results
fields_to_verify = ['weighted_volumerate_avg', 'weighted_buildrate_avg', "weighted_avg"]

# Verify the interpolation results
for filename in list_geojson_files(output_directory):
    output_file_path = os.path.join(output_directory, filename)
    df = gpd.read_file(output_file_path, encoding='utf-8-sig')

    for field in fields_to_verify:
        if field in df.columns:
            # Check for zeros in the interpolated fields
            num_zeros = len(df[df[field] == 0])
            num_non_zeros = len(df[df[field] != 0])
            total = len(df)
            if total > 0:  # To avoid division by zero
                percent_non_zeros = 100 * num_non_zeros / total
                print(f"File: {filename}, Field: {field}, Zeros: {num_zeros}, Non-Zeros: {num_non_zeros} -->({percent_non_zeros:.2f}%)")
            else:
                print(f"File: {filename}, Field: {field}, DataFrame is empty or field values are all zero.")
