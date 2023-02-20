# Assessing Standard Values of Houses in Tainan City
Through a data science project for the Finance and Taxation Bureau, Tainan City Government, the researcher model the spatial distribution of location adjustment parameters with Multiple Input CNN for assessing standard values of houses in Tainan City, Taiwan.

For "POIs with a smaller range of influence" and "POIs with a larger range of influence", a grid of 100m*100m is used as the basic unit, and the number of various POIs in each grid is used as the value of this grid, which is trained by CNN with various POI latitude and longitude data. For the numerical data of a single point, Linear Regression is used.

The features extracted by the three models (two CNNs, one Linear Regression) are combined, and then the fully connected layer is used to learn the feature of the location rate.
