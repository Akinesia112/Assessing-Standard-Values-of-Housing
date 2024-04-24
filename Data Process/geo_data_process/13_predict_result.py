import geopandas as gpd
import pandas as pd
from shapely import wkt

# Read the original CSV file into a DataFrame
df = pd.read_csv(r"D:\財稅\data\raw\meta_data\meta_data_updated_output.csv", encoding='utf-8-sig')


columns_to_keep = [
    "id",
     "105APV_weighted_avg", "105RAR_weighted_avg",
    "108APV_weighted_avg", "108RAR_weighted_avg",
    "111APV_weighted_avg", "111RAR_weighted_avg",
    "113APV_weighted_avg", 
    "geometry" ,  # Always keep the geometry column
    "預測值"
]

# Select only the desired columns
df = df[columns_to_keep]

# Assuming the 'geometry' column in the CSV contains WKT formatted strings, convert these to Shapely geometries
df['geometry'] = df['geometry'].apply(wkt.loads)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:3857')


geojson_path = r"D:\財稅\data\raw\meta_data\meta_data_updated_output_4.geojson"
gdf.to_file(geojson_path, driver='GeoJSON', encoding='utf-8-sig')

print("GeoJSON file has been saved.")