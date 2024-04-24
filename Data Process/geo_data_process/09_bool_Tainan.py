import geopandas as gpd
import os
import pandas as pd
from shapely import wkt

# 定义输入和输出文件夹路径
input_path = r"D:\財稅\data\raw\merged_data_all.csv"
output_directory = r"D:\財稅\data\raw\meta_data"   # 保存的文件夹
county_shapefile_path = r"D:\財稅\data\raw\Tainan_shp\Tainan.geojson"  # 縣市界

# 确保输出文件夹存在
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Load the CSV file
data = pd.read_csv(input_path, encoding='utf-8-sig')
# Convert WKT from EPSG3857 to geometry
data['geometry'] = data['WKT'].apply(wkt.loads)
# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry='geometry', crs='EPSG:3857')

# Load the Tainan GeoJSON
tainan = gpd.read_file(county_shapefile_path)
tainan = tainan.to_crs(epsg=3857)

# Perform the intersect operation
intersect = gpd.overlay(tainan, gdf, how='intersection')

# Save the intersect as GeoJSON
geojson_path = output_directory + r"\meta_data.geojson"
intersect.to_file(geojson_path, driver='GeoJSON')

# Save the intersection as CSV
csv_path = output_directory + r"\meta_data.csv"
intersect.drop('geometry', axis=1).to_csv(csv_path, index=False, encoding='utf-8-sig')

print("Files have been saved successfully.")

