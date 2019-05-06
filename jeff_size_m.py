# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:47:58 2019
updated 5.4.19
@author: trst9490
"""

import arcpy
from arcpy import env
import subprocess
from arcpy.sa import *
import numpy as np
import arcpy.sa as sa
import osgeo
import osgeo.ogr
from osgeo import ogr, osr, gdal, gdalconst
import osgeo.gdal
osgeo.gdal.GetDriverByName
import os
import math

# set workspace environment
arcpy.env.workspace = r"D:\master_4_27"
arcpy.env.overwriteOutput = 1
#import Jeff county layer 
#jeff = r"D:\master_4_27\data\Jeff_parcel2.shp"
#colo_dem = r"D:\master_4_27\grids\dem_utm_120m"
#nlcd = r"D:\master_4_27\grids\nlcd_utm" #inRaster


#colo_dem_ras = sa.Raster(colo_dem)
#colo_Arr = arcpy.RasterToNumPyArray(colo_dem_ras)

def select_size(jeff):
    with arcpy.da.UpdateCursor(jeff, ['SHAPE_AREA']) as cursor2:
        for row in cursor2:
            for area in row:
                if area < 1307000:
                    cursor2.deleteRow()    
                
    del row
    del area 
    del cursor2
    
    #does it need to return this tho?
    return jeff

