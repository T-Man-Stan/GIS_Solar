# -*- coding: utf-8 -*-
"""
Created by Trevor Stanley, Avra Saslow, and Xingying Huang
GEOG 4303 Final Project 5.7.19

Main script
"""
# import necessary modules for the analysis
print 'importing Libraries & Modules'

import arcpy
from arcpy import env
from arcpy.sa import *
import numpy as np
import arcpy.sa as sa
import osgeo
import osgeo.ogr
from osgeo import ogr, osr
import os
import math

#import All the modules!
import suitability
import jeff_size_m
import floodplain_m
#Set workspace environment
print 'setting workspace'
#set env properties
arcpy.env.workspace = r"D:\Deliverable"
env.overwriteOutput = 1
arcpy.CheckOutExtension("Spatial")

#designant variable names as certain files within the source_data folder
jeff = r"D:\Deliverable\source_data\jeff_parcel_13N.shp"
colo_dem = r"D:\Deliverable\source_data\dem_utm_120m"
nlcd = r"D:\Deliverable\source_data\nlcd_utm_13n" #inRaster
colorivers = r"D:\Deliverable\source_data\colo_rivers.shp"

# 1. select parcels larger than 30 acres; consider passing in variable that the user can specify
#------------------------------------------------------------------------------------------------
jeff_size = jeff_size_m.select_size(jeff)

# 2. create buffers for electric infrastructure
#------------------------------------------------------------------------------------------------
lines = r"D:\Deliverable\source_data\colo_trans_13N.shp"#transmission lines 
stations = r"D:\Deliverable\source_data\colo_subs_13N.shp"#substations

arcpy.Buffer_analysis(lines, r"D:\Deliverable\source_data\lineBuff", "3218.88 meters")
arcpy.Buffer_analysis(stations, r"D:\Deliverable\source_data\pointBuff", "3218.88 meters")

line_buff = r"D:\Deliverable\source_data\lineBuff.shp"
point_buff = r"D:\Deliverable\source_data\pointBuff.shp"

# 3. Select Agricultural and P-D zoned parcels
#---------------------------------------------------------------------------------------------
print "*******Part 6: Select Argricultural district from Jeff Zoning *********"
#in_features: jeff_clipZ
jeff_Agri = r"D:\Deliverable\source_data\jeff_Agri.shp"
jeffZ = r"D:\Deliverable\source_data\jeff_zone_13N.shp"
agri = """"ZTYPE" = 'A-1' OR "ZTYPE" = 'A-2' OR "ZTYPE" = 'A-35' OR "ZTYPE" = 'P-D'"""
arcpy.Select_analysis(jeffZ, jeff_Agri,agri )

# 5. Suitability Anlaysis of NLCD, Slope, & Aspect
#----------------------------------------------------------------------------------------------
#resample and naming for nlcd
arcpy.Resample_management(nlcd, r"D:\Deliverable\source_data\nlcd120utm13n", "120 120", "NEAREST")

#mask and naming for dem that will be used for slope and aspect
outExtractByMask = ExtractByMask(colo_dem, jeff)
outExtractByMask.save("D:\Deliverable\source_data\dem_utm_120m"+"clip.tif")
jeff_dem = r"D:\Deliverable\source_data\dem_utm_120mclip.tif"

#rasterize and make NP array from the clipped colo_dem for the jeff county dem
jeff_dem_ras = sa.Raster(jeff_dem)
jeff_Arr = arcpy.RasterToNumPyArray(jeff_dem_ras)

#derive aspect and name from the jeff dem, the variable will be pased to asp_suit
outAspect = Aspect(jeff_dem)
outAspect.save("D:\Deliverable\source_data\dem_utm_120mclip"+"_aspect.tif")
jeff_asp = "D:\Deliverable\source_data\dem_utm_120mclip_aspect.tif"

#derive slope and name from the previous file, the variable will be pased to slope_suit
outSlope = Slope("D:\Deliverable\source_data\dem_utm_120mclip_aspect.tif", "PERCENT_RISE")
outSlope.save("D:\Deliverable\source_data\dem_utm_120mclip_aspect"+"slope.tif")
jeff_slope = r"D:\Deliverable\source_data\dem_utm_120mclip_aspect"+"slope.tif"

#set variable input names and rasterize
nlcd2 = r"D:\Deliverable\source_data\nlcd120utm13n"
jeff_dem_slop = sa.Raster(jeff_slope)
jeff_dem_asp = sa.Raster(jeff_asp)

slop_Arr = arcpy.RasterToNumPyArray(jeff_dem_slop)
slop_Arr[slop_Arr <= 0] = 0

#send the above variable names to the suitability functions;
#these functions return NP arrays that have been selected/smoothed for via the focal mean function
nlcd_veg_suit = suitability.nlcd_suit(nlcd2)
slope_suit = suitability.slope_suit(jeff_dem_slop)
aspect_suit = suitability.asp_suit(jeff_dem_asp) 

final_suit_grid = suitability.np_2_raster(jeff_dem_ras, jeff_dem_slop, aspect_suit, slope_suit, nlcd_veg_suit, slop_Arr)
#change below name to be concatenated with the passed variable from user (the aspect value)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
final_suit_grid.save("suitOut_90")


# 6. Intersect all of these criteria layers and rasterize the output
#    Then create a ZST of the intersect and the suitability dem; this will be joined later with the orginal parcel data
#----------------------------------------------------------------------------------------------
input_list = [jeff_Agri, jeff, line_buff, point_buff]

#The intersect of these areas are where solar sites can potentially be built (i.e. the non-negotiable criteria have been met)
arcpy.Intersect_analysis(input_list, r"D:\Deliverable\source_data\jeff_intersect.shp", "ALL")

#rasterize the intersect:
inFeatures = r"D:\Deliverable\source_data\jeff_intersect.shp"
valField = "PIN"
outRaster = r"D:\Deliverable\source_data\intersect_dem"
assignmentType = "CELL_CENTER"

arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, 
                                 assignmentType)

# placeholder for ouput from floodplain analysis, erase these areas from intersect
#---------------------------------------------------------------------------------------------------------

#set variable input names and rasterize
jeff_dem_slop = sa.Raster(r"D:\Deliverable\source_data\dem_utm_120mclip_aspectslope.tif")

#Call floodplain function from the floodplane module
floodplain_m.floodplain(jeff_dem_slop, colorivers)

#name variables with the relvant outputted files from the above function
steepBuff = r"D:\Deliverable\steepBuff.shp"
flatBuff = r"D:\Deliverable\flatBuff.shp"

#erase these areas as they are floodplanes that solar arrays cannot be developed in
arcpy.Erase_analysis(r"D:\Deliverable\source_data\jeff_intersect.shp", steepBuff, r"D:\Deliverable\source_data\jeff_intersect1.shp")
arcpy.Erase_analysis(r"D:\Deliverable\source_data\jeff_intersect1.shp", flatBuff, r"D:\Deliverable\source_data\jeff_intersect2.shp")


# Rasterize intersect & Perform ZST with intersect and suitability grids
#------------------------------------------------------------------------------------------------------------
#rasterize the intersect:
inFeatures = r"D:\Deliverable\source_data\jeff_intersect2.shp"
valField = "PIN"
outRaster = r"D:\Deliverable\source_data\inter_fp_dem"
assignmentType = "CELL_CENTER"

# Execute PolygonToRaster
arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, 
                                 assignmentType)

#This ZST joins the inter_fp_dem with the combined suitability dem values (based on "Maximum")
#change "suitOut_90" to the "test_suid_mod" file name;
ZST = ZonalStatisticsAsTable(r"D:\Deliverable\source_data\inter_fp_dem", "PIN",  r"D:\Deliverable\suitOut_90",
                                  r"D:\Deliverable\source_data\ZST_dem", "NODATA", "Maximum")


# 7. Perform final joins so that suitability output raster has correct parcel data fields
#----------------------------------------------------------------------------------------------
inFeatures = r"D:\Deliverable\source_data\inter_fp_dem"
joinField = "PIN"
joinTable = r"D:\Deliverable\source_data\ZST_dem"
fieldList = ["MAX"]
# Join two feature classes by the zonecode field and only carry over the land use and land cover fields
arcpy.JoinField_management(inFeatures, joinField, joinTable, joinField, 
                           fieldList)


#Final Output of suitable sites is named "inter_fp_dem"; 376 sites shouldv'e been outputted when aspect ratio is set at 90%
inFeatures = r"D:\Deliverable\source_data\inter_fp_dem"
joinField = "PIN"
joinTable = r"D:\Deliverable\source_data\jeff_parcel_13N.shp"
fieldList = ["SPN", "X_COORD","Y_COORD","OWNNAM","OWNNAM2","MAILSTRNBR","MAILSTRDIR","MAILSTRNAM","MAILSTRTYP","MAILSTRUNT","MAILCTYNAM","MAILSTENAM","MAILZIP5","PRPSTRNBR","PRPSTRDIR","PRPSTRNAM","PRPSTRTYP","PRPSTRUNT","PRPCTYNAM","PRPSTENAM","PRPZIP5","NHDNAM","SHAPE_AREA"]

arcpy.JoinField_management(inFeatures, joinField, joinTable, joinField, 
                           fieldList)


#User Input stuff
#usInpt = raw_input("enter a float number like 20.0 or 80.0 betweeon 0.0 and 100.0: ")




