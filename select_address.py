import pickle
import pandas as pd
from shapely.geometry import Point, shape
from zipfile import ZipFile
import shapefile
from StringIO import StringIO
import fiona

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

print residential_address.shape

#load polygons
zip_file_name = "zip://input/cb_2017_53_tract_500k.zip"

with fiona.open(zip_file_name) as shp:
    polygons = [poly for poly in shp]

samples = residential_address.sample(10)

print samples

lat = samples.iloc[[0]]['LAT']
lon = samples.iloc[[0]]['LON']

print lat.values[0],lon.values[0]

matched = coordinates_to_census_tract(lon, lat, polygons)

print matched

print samples.iloc[[0]]
