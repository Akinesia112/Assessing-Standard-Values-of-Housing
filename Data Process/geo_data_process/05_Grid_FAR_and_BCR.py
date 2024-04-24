'''

Notice: This script is for calculating the Floor Area Ratio (FAR) (容積率) and Building Coverage Ratio (BCR) (建蔽率) for each grid in Tainan City, Taiwan.

Due to the limitations of the data, the FAR and BCR values are only available for urban planning areas in Taiwan. 
Thus, the FAR and BCR values are not available for non-urban planning areas. This is because the FAR and BCR values are regulated by urban planning regulations.

Therefore, some areas may not have FAR and BCR values, and some areas may have extremely high FAR or BCR values due to special zoning regulations.

Specifically, the steps are as follows:
1. Use the clip function to cut the FAR data into polygons based on the grid.
2. Use the filter function to filter out the polygons that have 0 FAR and 0 BCR values.
3. Use the area function to calculate the area of each polygon.
4. Convert the polygon to a centroid point.
5. Use the "sjoin function" to calculate the sum of the (area * FAR) or (area * BCR) for each point in a single grid based on the number of points in the polygon.
6. Get the sum of the area for each point in a single grid based on the number of points in the polygon by using the "sjoin function".
7. Divide the results from steps 5 and 6 to get the weighted FAR or BCR.


注意!!!!!
因為台灣只有都市計畫區有建蔽率與容積率，所以在土地使用分區(容積建蔽)這個資料中，有很多地區沒有polygon，那是非都市計畫區，沒有polygon很正常。
然後都市計畫區某些區域突然容積率爆高也是正常的，因為那是特許容積率，所以不要驚訝。

步驟:
1. 用裁切把容積率資料依照網格切成一格一格的polygon
2. 過濾掉容積率跟建蔽率都為0的polygon
3. 計算每個polygon的面積
4. 將polygon轉換為質心point
5. 用「多邊形內點的數量」來計算單一網格內每個point的(面積*容積率)或(面積*建蔽率)總和
6. 用「多邊形內點的數量」來計算單一網格內每個point的面積總和
7. 將5,6兩個結果相除，得到面積加權容積率或面積加權建蔽率
'''

import geopandas as gpd
import pandas as pd
import numpy as np
import re

# Read the Grid and RawData files from the specified path
polygons = gpd.read_file(r'D:\財稅\data\台南圖台土地使用分區(容積建蔽)-20240326T153902Z-001\台南圖台土地使用分區(容積建蔽)\台南圖台土地使用分區.shp')  # The .shp file path that contains the FAR and BCR values
grid = gpd.read_file(r'D:\財稅\data\grid-20240325T120505Z-001\grid\grid_shp.shp')  # The .shp file path of the grid data

# Set the CRS for the grid, assuming you know it is EPSG:3857
if grid.crs is None:
    grid.set_crs('EPSG:3857', inplace=True)

# Ensure the grid and polygons use the same CRS, to_crs(3857) is used to convert the CRS to EPSG:3857
grid = grid.to_crs(3857)
polygons = polygons.to_crs(3857)

# Step 1. Use the clip function to cut the FAR data into polygons based on the grid
# 步驟 1. 使用裁切將容積率資料按照網格切成一格一格的polygon
clipped = gpd.overlay(polygons, grid, how='intersection')
print(clipped.head())

'''
Notice!!!!!

The FAR and BCR data in the polygons may contain Chinese characters or symbols.
Ensure that the values in the 'VOLUMERATE' and 'BUILDRATE' columns are numeric by removing any Chinese characters or symbols.
Please use the unique() function to determine the form of the Chinese characters or symbols in the FAR and BCR values.
If necessary, modify the convert_values_ignore_all_nonnumeric(values) function to remove these symbols and keep only the numbers so that they can be converted to floating-point numbers without missing a bunch of values.


注意!!!!!

都計區中的容積建蔽，有些值會夾雜中文或符號，要去掉這些東西，只保留數字，這樣才能順利轉換為浮點數，而不會缺失一堆值。
請用unique()函數判斷你的資料中夾雜中文或符號的形式，然後如有必要就修改以下convert_values_ignore_all_nonnumeric(values)，將那些符號去掉，只保留數字。
'''

#print all kinds of values in 'VOLUMERATE' and 'BUILDRATE' that are not NaN
print("VOLUMERATE:", clipped['VOLUMERATE'].unique())
print("BUILDRATE:", clipped['BUILDRATE'].unique())

# Define the a comprehensive function to convert the strings to floating-point numbers, returning NaN if the string does not contain numbers
def convert_values_ignore_all_nonnumeric(values):
    processed_values = []
    for value in values:
        if pd.isnull(value):  # 如果值是NaN，添加NaN作为占位符
            processed_values.append(np.nan)
        else:
            # 使用正則表達式找到所有數字，並將其轉換為浮點數
            # 對於複雜表達式，可以使用re.compile()函數編譯正則表達式，以提高效率
            numeric_part = re.findall(r'\d+', value)
            if numeric_part:
                # 如果找到數字，將第一組數字轉換為浮點數
                numeric_value = float(numeric_part[0])
                processed_values.append(numeric_value)
            else:
                # 如果找不到數字，添加NaN作為占位符
                processed_values.append(np.nan)
    return processed_values

# 使用這個綜合性函數來處理'VOLUMERATE'和'BUILDRATE'欄位
volumerate_combined_conversion = convert_values_ignore_all_nonnumeric(clipped['VOLUMERATE'])
buildrate_combined_conversion = convert_values_ignore_all_nonnumeric(clipped['BUILDRATE'])

# 顯示前10個轉換後的值
volumerate_combined_conversion[:10], buildrate_combined_conversion[:10]

clipped['VOLUMERATE'] = volumerate_combined_conversion

clipped['BUILDRATE'] = buildrate_combined_conversion

# 步驟 2. 過濾掉容積率和建蔽率都為0的polygon
filtered = clipped[(clipped['VOLUMERATE'] > 0) | (clipped['BUILDRATE'] > 0)]  # 使用或(|)關係，因為要保留容積率或建蔽率大於0的polygon

# 步驟 3. 計算每個polygon的面積
filtered['AREA'] = filtered.geometry.area
print(filtered.head())

# 步驟 4. 將polygon轉換為質心point
filtered['centroid'] = filtered.geometry.centroid

# 步驟 5. 使用空間加入找出每個點落在哪個網格內
joined = gpd.sjoin(filtered, grid, how='inner', op='within')
print(joined.head())

joined['AREA'] = joined['AREA'].astype(float)
joined['VOLUMERATE'] = joined['VOLUMERATE'].astype(float)
joined['BUILDRATE'] = joined['BUILDRATE'].astype(float)

# 步驟 6. 計算單一網格內每個point的面積總和
sum_area = joined.groupby('index_right')['AREA'].sum()
print(sum_area.head())

# 步驟 7. 計算面積加權容積率和建蔽率
joined['weighted_volumerate'] = joined['VOLUMERATE'] * joined['AREA']
joined['weighted_buildrate'] = joined['BUILDRATE'] * joined['AREA']
print(joined.head())

# 步驟 8. 使用 groupby 計算每個網格的加權容積率和建蔽率總和
sum_weighted_volumerate = joined.groupby('index_right')['weighted_volumerate'].sum()
sum_weighted_buildrate = joined.groupby('index_right')['weighted_buildrate'].sum()

# 步驟 9. 計算加權平均值
result = pd.DataFrame({
    'weighted_volumerate_avg': sum_weighted_volumerate / sum_area,
    'weighted_buildrate_avg': sum_weighted_buildrate / sum_area
}).reset_index()

# 步驟 10. 合併回網格數據
result = grid.merge(result, left_index=True, right_on='index_right', how='left')

# 步驟 11. 填充缺失值
result[['weighted_volumerate_avg', 'weighted_buildrate_avg']] = result[['weighted_volumerate_avg', 'weighted_buildrate_avg']].fillna(0)

# print !=0 的值
print(result[result['weighted_volumerate_avg'] != 0].head())
print(result[result['weighted_buildrate_avg'] != 0].head())

# 計算容積率和建蔽率的平均值中的非0值比率並印出
print(100 * len(result[result['weighted_volumerate_avg'] != 0]) / len(result))
print(100 * len(result[result['weighted_buildrate_avg'] != 0]) / len(result))

# 步驟 12. 印出结果
print(result.head())

# 步驟 13. 保存到文件
result.to_file(r"D:\財稅\data\raw\Grid\113_FAR_and_BCR_Grid.geojson", driver='GeoJSON', encoding='utf-8-sig')


