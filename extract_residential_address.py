from zipfile import ZipFile
from StringIO import StringIO
import shapefile
import geopandas as gpd
from shapely.geometry import shape
import osr
import pandas as pd
import pickle

pd.set_option('display.expand_frame_repr', False)

def read_shp_zip(zip_file_name):
    """
    read zipped shapefile to memory, and convert to geodataframe
    """
    zip_file = ZipFile(open(zip_file_name,'rb'))
    filenames = [y for y in sorted(zip_file.namelist()) for ending in ['dbf', 'prj', 'shp', 'shx']\
                 if y.endswith(ending) and not y.startswith('_')]
    print filenames
    dbf, prj, shp, shx = [StringIO(zip_file.read(filename)) for filename in filenames]
    r = shapefile.Reader(shp=shp, shx=shx, dbf=dbf)

    attributes, geometry = [], []
    field_names = [field[0] for field in r.fields[1:]]
    for row in r.shapeRecords():
        geometry.append(shape(row.shape.__geo_interface__))
        attributes.append(dict(zip(field_names, row.record)))

    #proj4_string = osr.SpatialReference(prj.read()).ExportToProj4()
    gdf = gpd.GeoDataFrame(data = attributes, geometry = geometry)
    return gdf

all_address = read_shp_zip("input/KC_address.zip")
residential_address = all_address.query('SITETYPE_D == "Single Family"')
residential_address.to_pickle('input/KC_residential.pickle')
