import geopandas as gpd
from shapely.geometry import shape
from shapely.ops import nearest_points

# Load the train station data and the grid data
train_stations_gdf = gpd.read_file(r"D:\財稅\data\raw\2022_POI\geojsons\traffic_train_station.geojson")
# grid_gdf = gpd.read_file(r"D:\財稅\data\raw\meta_data\meta_data.geojson")
grid_gdf = gpd.read_file(r"D:\財稅\data\raw\merged_data_all_square.geojson")

# Reproject the data if necessary (the provided coordinates seem to be in CRS84)
train_stations_gdf = train_stations_gdf.to_crs(epsg=3857)
grid_gdf = grid_gdf.to_crs(epsg=3857)

# Add a new column for the nearest station distance
grid_gdf['nearest_station_dist'] = None

# Calculate the nearest train station distance for each grid cell
for index, grid_cell in grid_gdf.iterrows():
    nearest_dist = float(min(train_stations_gdf.distance(grid_cell.geometry)))
    
    grid_gdf.at[index, 'nearest_station_dist'] = nearest_dist
    print(f"Processed {index}")

grid_gdf = grid_gdf.to_crs(epsg=4326)

# Save the updated grid data
grid_gdf.to_file(r"D:\財稅\data\raw\meta_data\meta_data_updated_4326.geojson", driver='GeoJSON', encoding='utf-8-sig')

# Also save to CSV if needed
grid_gdf.to_csv(r"D:\財稅\data\raw\meta_data\meta_data_updated_4326.csv", index=False, encoding='utf-8-sig')
