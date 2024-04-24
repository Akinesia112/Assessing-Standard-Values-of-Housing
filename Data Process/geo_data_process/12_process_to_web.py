import geopandas as gpd
from shapely.geometry import Polygon, Point, LinearRing
import json

# Read the original GeoJSON file into a GeoDataFrame
# gdf = gpd.read_file(r"D:\財稅\data\raw\meta_data\meta_data_web_test_avg_only_Tainan.geojson")

gdf = gpd.read_file(r"D:\財稅\data\raw\meta_data\meta_data_updated_output_only_Tainan.geojson")

#  Convert the GeoDataFrame to EPSG:4326
gdf = gdf.to_crs(epsg=4326)

# Rename the columns to remove the '_weighted_avg' suffix
columns_to_rename = {
    '105APV_weighted_avg': '105APV',
    '105RAR_weighted_avg': '105RAR',
    '108APV_weighted_avg': '108APV',
    '108RAR_weighted_avg': '108RAR',
    '111APV_weighted_avg': '111APV',
    '111RAR_weighted_avg': '111RAR',
    '113APV_weighted_avg': '113APV',
    '預測值':'Predict'
}
gdf.rename(columns=columns_to_rename, inplace=True)

# Define a function to reduce the precision of the coordinates
def reduce_precision(geometry, precision=4):
    if geometry.geom_type == 'Polygon':
        # Correctly handle the exterior and interior coordinates
        exterior_coords = [(round(x, precision), round(y, precision)) for x, y in geometry.exterior.coords]
        interiors_coords = [[(round(x, precision), round(y, precision)) for x, y in interior.coords] for interior in geometry.interiors]
        new_geometry = Polygon(LinearRing(exterior_coords), [LinearRing(interior) for interior in interiors_coords])
        return new_geometry
    elif geometry.geom_type == 'Point':
        # Round the coordinates to the specified precision
        new_coordinates = (round(geometry.x, precision), round(geometry.y, precision))
        new_geometry = Point(new_coordinates)
        return new_geometry
    return geometry

# Apply the function to the 'geometry' column
gdf['geometry'] = gdf['geometry'].apply(reduce_precision)
gdf['Predict'] = gdf['Predict'].round(1)


# Write the selected data to a new GeoJSON file
# gdf.to_file(r"D:\財稅\data\raw\meta_data\meta_data_web_test_avg_only_Tainan_4326.geojson", driver='GeoJSON')
gdf.to_file(r"D:\財稅\data\raw\meta_data\meta_data_updated_output_web_test_only_Tainan.geojson", driver='GeoJSON')
