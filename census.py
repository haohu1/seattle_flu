from census_mapper import *
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
import pysal, descartes

#census_mapper functions from https://github.com/agaidus/census_data_extraction/blob/master/census_mapper.py

pd.set_option('display.expand_frame_repr', False)

#WA shapefile
zipped_shp_url = 'http://www2.census.gov/geo/tiger/GENZ2016/shp/cb_2016_53_tract_500k.zip'

all_wa_tract_geo = zip_shp_to_gdf(zipped_shp_url)
king_tract_geo = all_wa_tract_geo[all_wa_tract_geo.COUNTYFP=='033'].to_crs(epsg=3689).set_index("GEOID")
print king_tract_geo.head()
king_tract_geo = king_tract_geo['geometry']

king_tract_demographics = get_census_variables('5fec6ad56b12777903bce444563eed6a4501a492',
                                                2016, 'acs/acs5', 'tract',
                                                {'county':'033', 'state':'53'},
                                                ['B01003_001E', 'B01001_001E'], ['population', 'population2'])['population'].dropna().astype(int)

print king_tract_demographics.head()
king_gdf = gpd.GeoDataFrame(geometry = king_tract_geo, data = king_tract_demographics)
print king_gdf.head()
fig, ax = plt.subplots(figsize=(10,10))
ax.set(aspect='equal', xticks=[], yticks=[])
king_gdf.plot(column= 'population', ax = ax, scheme='QUANTILES', cmap='Purples', legend=True)
plt.title('King County, WA - Population by Census Tract', size = 14)
plt.savefig('King_County_pop.png',bbox_inches='tight',dpi=100)

#load addresses
king_address_geo = zip_shp_to_gdf()
