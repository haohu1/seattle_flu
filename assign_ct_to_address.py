import pickle
import pandas as pd
from shapely.geometry import Point, shape
from zipfile import ZipFile
import shapefile
from StringIO import StringIO
import fiona
import numpy as np

pd.set_option('display.expand_frame_repr', False)

def coordinates_to_census_tract(lon, lat, polygons):
    mypoint = Point(lon, lat)
    poly_idx = [i for i, poly in enumerate(polygons)
                if mypoint.within(shape(poly['geometry']))]

    if not poly_idx:
        return None
    else:
        # Take first polygon that overlaps since may overlap with several if on border
        match = polygons[poly_idx[0]]
        return match['properties']['GEOID']

print "read dataset."
residential_address = pd.read_pickle('input/KC_residential.pickle')
print "read complete."

residential_address['GEOID'] = ""

#load polygons
zip_file_name = "zip://input/cb_2017_53_tract_500k.zip"

with fiona.open(zip_file_name) as shp:
    polygons = [poly for poly in shp]

for index, row in residential_address.iterrows():
    if index % 100 == 0:
        print index
    residential_address.loc[index,'GEOID']= coordinates_to_census_tract(row['LON'], row['LAT'], polygons)

residential_address.to_pickle('input/KC_residential_censustract.pickle')
