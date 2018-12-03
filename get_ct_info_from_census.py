from census_mapper import *
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
import pysal, descartes
import pickle

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
                                                ['B01003_001E', 'B01001_003E', 'B01001_004E',
                                                'B01001_005E', 'B01001_006E', 'B01001_007E',
                                                'B01001_008E', 'B01001_009E', 'B01001_010E',
                                                'B01001_011E', 'B01001_012E', 'B01001_013E',
                                                'B01001_014E', 'B01001_015E', 'B01001_016E',
                                                'B01001_017E', 'B01001_018E', 'B01001_019E',
                                                'B01001_020E', 'B01001_021E', 'B01001_022E',
                                                'B01001_023E', 'B01001_024E', 'B01001_025E',
                                                'B01001_027E', 'B01001_028E', 'B01001_029E',
                                                'B01001_030E', 'B01001_031E', 'B01001_032E',
                                                'B01001_033E', 'B01001_034E', 'B01001_035E',
                                                'B01001_036E', 'B01001_037E', 'B01001_038E',
                                                'B01001_039E', 'B01001_040E', 'B01001_041E',
                                                'B01001_042E', 'B01001_043E', 'B01001_044E',
                                                'B01001_045E', 'B01001_046E', 'B01001_047E',
                                                'B01001_048E', 'B01001_049E'],
                                                ['total', 'M0-5', 'M5-9', 'M10-14', 'M15-17',
                                                'M18-19', 'M20-20', 'M21-21', 'M22-24',
                                                'M25-29', 'M30-34', 'M35-39', 'M40-44',
                                                'M45-49', 'M50-54', 'M55-59', 'M60-61',
                                                'M62-64', 'M65-66', 'M67-69', 'M70-74',
                                                'M75-79', 'M80-84', 'M85-120',
                                                'F0-5', 'F5-9', 'F10-14', 'F15-17',
                                                'F18-19', 'F20-20', 'F21-21', 'F22-24',
                                                'F25-29', 'F30-34', 'F35-39', 'F40-44',
                                                'F45-49', 'F50-54', 'F55-59', 'F60-61',
                                                'F62-64', 'F65-66', 'F67-69', 'F70-74',
                                                'F75-79', 'F80-84', 'F85-120'])
king_tract_demographics.to_pickle('input/KC_CT_age_gender.pickle')
