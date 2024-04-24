import geopandas as gpd
from shapely.geometry import box

# Read the Grid and RawData files

gdf = gpd.read_file(r"D:\財稅\data\raw\Grid.csv", encoding='utf-8-sig')
df = gpd.read_file(r"D:\財稅\data\raw\RAR_transformed.csv", encoding='utf-8-sig')
print(gdf.head())
print(df.head())

# Ensure the boundary of the grid data is float
for col in ['left', 'bottom', 'right', 'top']:
    gdf[col] = gdf[col].astype(float)

# Create the geometry shape of the grid
gdf['geometry'] = gdf.apply(lambda row: box(row['left'], row['bottom'], row['right'], row['top']), axis=1)
gdf = gpd.GeoDataFrame(gdf, geometry='geometry', crs='EPSG:3857')

# Ensure the CRS of the RawData is correct for the spatial join of the points in the grid data, and the grid data itself is a GeoDataFrame
df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['X軸_3857'], df['Y軸_3857']), crs='EPSG:3857')
print(df.head())

# Use spatial join to find out which grid each point falls into
joined = gpd.sjoin(df, gdf, how='inner', op='within')
print(joined.head())

# The columns to be used for the calculation:
# 105年評定之地段率, 108年評定之地段率, 111年評定之地段率, 最大折舊年數, 105公告現值, 108公告現值, 111公告現值, 113公告現值
joined['113公告現值'] = joined['113公告現值'].astype(float)

# Calculate the number of points and the sum of the weighted values within each grid
count_weighted = joined.groupby('index_right').agg(
    point_count=('geometry', 'count'), 
    weighted_sum=('113公告現值', 'sum')
).reset_index()

# Add a weighted average column to avoid division by 0
count_weighted['weighted_avg'] = count_weighted.apply(
    lambda row: row['weighted_sum'] / row['point_count'] if row['point_count'] > 0 else 0, axis=1)

# Merge the result back into the grid data
result = gdf.merge(count_weighted, left_index=True, right_on='index_right', how='left')

# Fill missing values with 0 for the 'point_count', 'weighted_sum', and 'weighted_avg' columns
result[['point_count', 'weighted_sum', 'weighted_avg']] = result[['point_count', 'weighted_sum', 'weighted_avg']].fillna(0)

# Ensure that 'point_count', 'weighted_sum' are floats
result[['point_count', 'weighted_sum']] = result[['point_count', 'weighted_sum']].astype(float)

# Show the values that are not 0
print(result.head())

# Save the result to a GeoJSON file
result.to_file(r"D:\財稅\data\raw\113APV_Grid_Count_and_Weighted.geojson", driver='GeoJSON', encoding='utf-8-sig')
