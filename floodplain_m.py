'''***************************************************************
Author: Avra Saslow, Trevor Stanley, Xingying Huang
Date: 5.4.19
Purpose: Floodplain function
***************************************************************'''
#libraries
import numpy as np
import arcpy
from arcpy import env
import arcpy.sa as sa
from math import sqrt
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *
import pandas as pd

#workspace
env.workspace = r"D:\Deliverable"
env.overwriteOutput = 1

jeff_dem = r"D:\Deliverable\source_data\dem_utm_120mclip.tif"
colorivers = r"D:\Deliverable\source_data\colo_rivers.shp"
#county = r"D:\Deliverable\source_data\jeff_parcel_13N.shp"


#set variable input names and rasterize

def floodplain(slop_dem, colorivers):
    
    
#    jeff_dem_slop = sa.Raster(r"D:\Deliverable\source_data\dem_utm_120mclip_aspectslope.tif")
    dem = r"D:\Deliverable\source_data\dem_utm_120mclip.tif"
    jeff_dem_ras = sa.Raster(dem)

    llpnt2 = jeff_dem_ras.extent.lowerLeft
    demSize2 = jeff_dem_ras.meanCellHeight
    
    slop_Arr = arcpy.RasterToNumPyArray(slop_dem)
    slop_Arr[slop_Arr <= 0] = 0
    
    flat_grid = np.where((slop_Arr <= 25.0),1,0)
   
    flatRaster = arcpy.NumPyArrayToRaster(flat_grid,llpnt2,demSize2,demSize2)
#    steepRaster = arcpy.NumPyArrayToRaster(steep_grid,llpnt,demSize,demSize)
#   
    arcpy.Delete_management("flat_FP")
    arcpy.DefineProjection_management(flatRaster,jeff_dem_ras.spatialReference)
    flatRaster.save('flat_FP')
    
#    floodplain(jeff_dem, colorivers)
    
    
    ZST = ZonalStatisticsAsTable(r"D:\Deliverable\source_data\intersect_dem", "PIN",  r"D:\Deliverable\flat_fp",
                                      r"D:\Deliverable\ZST_fp_dem", "NODATA", "Maximum")
    
    
    # 7. Perform final joins so that suitability output raster has correct parcel data
    #----------------------------------------------------------------------------------------------
    inFeatures = r"D:\Deliverable\source_data\intersect_dem"
    joinField = "PIN"
    joinTable = r"D:\Deliverable\ZST_fp_dem"
    fieldList = ["MAX"]
    # Join two feature classes by the zonecode field and only carry over the land use and land cover fields
    arcpy.JoinField_management(inFeatures, joinField, joinTable, joinField, 
                               fieldList)
    
    arcpy.RasterToPolygon_conversion(r"D:\Deliverable\source_data\intersect_dem", r"D:\Deliverable\source_data\intersect_dem"+".shp", "NO_SIMPLIFY", "MAX")
    
    
    inter_steep = r"D:\Deliverable\source_data\inter_steep.shp"
    inter_shp = r"D:\Deliverable\source_data\intersect_dem.shp"
    agri = """"gridcode" = 0 """
    arcpy.Select_analysis(inter_shp, inter_steep,agri)
    
    inter_flat = r"D:\Deliverable\source_data\inter_flat.shp"
    inter_shp = r"D:\Deliverable\source_data\intersect_dem.shp"
    agri = """"gridcode" = 1 """
    arcpy.Select_analysis(inter_shp, inter_flat,agri )
    
    arcpy.Clip_analysis(colorivers, inter_flat, r"D:\Deliverable\flatClip2.shp")
    arcpy.Clip_analysis(colorivers, inter_steep, r"D:\Deliverable\steepClip2.shp")
    
    arcpy.Delete_management("flatBuff")
    arcpy.Buffer_analysis(r"D:\Deliverable\flatClip2.shp", "flatBuff", "400 meters")
    arcpy.Delete_management("steepBuff")
    arcpy.Buffer_analysis(r"D:\Deliverable\steepClip2.shp", "steepBuff", "150 meters")
