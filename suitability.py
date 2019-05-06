# -*- coding: utf-8 -*-
"""
Created by Trevor Stanley, Avra Saslow, and Xingying Huang
GEOG 4303 Final Project 5.7.19
updated 5.4.19
Suitability module
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

arcpy.env.workspace = r"D:\Deliverable"
arcpy.env.overwriteOutput = 1
#import Jeff county layer 
jeff = r"D:\Deliverable\source_data\jeff_parcel_13N.shp"
colo_dem = r"D:\Deliverable\source_data\dem_utm_120m"
nlcd = r"D:\Deliverable\source_data\nlcd_utm_13n" #inRaster
arcpy.CheckOutExtension("Spatial")

def focalM(nparr):

    pGrid = np.zeros(nparr.shape).astype(float)
    for i in range (4,np.size(nparr,1)-5):
        for j in range (5,np.size(nparr,0)-6):
            sum = 0.0
            # now we will loop through our moving-window
            for ii in range(i-4,i+5):
                for jj in range(j-5,j+6):
                    sum = sum + nparr[jj,ii]
            pGrid[j][i] = float(sum/99.0)*100.0 
            #pGrid[j,i]=sum
    return pGrid

def nlcd_suit(nlcd2):
    jeffNlcd = ExtractByMask(nlcd2, jeff)
    jeffNlcd.save(r"D:\Deliverable\source_data\nlcd_120"+"clp2")
    
    jeff_nlcd_dem = r"D:\Deliverable\source_data\nlcd_120clp2"
    
    jeff_nlcd_ras = sa.Raster(jeff_nlcd_dem)
    jeff_nlcd_Arr = arcpy.RasterToNumPyArray(jeff_nlcd_ras)
    #jeff_nlcd_Arr[jeff_nlcd_Arr <= 0] = 0
    
    jeff_nlcd_grid = np.where((jeff_nlcd_Arr == 52)|(jeff_nlcd_Arr == 71)|(jeff_nlcd_Arr == 81)|(jeff_nlcd_Arr == 82),1,0)
    veg = focalM(jeff_nlcd_grid)
    veg_A = np.zeros(jeff_nlcd_grid.shape).astype(float)
    veg_A = np.where((veg > 50.0),1,0).astype(float)
    return veg_A
    
#Slope (below)
#---------------------------------------------------------------------------------------------

def slope_suit(jeff_dem_slop):
    slop_Arr = arcpy.RasterToNumPyArray(jeff_dem_slop)
    slop_Arr[slop_Arr <= 0] = 0
    
    slop_grid = np.where((slop_Arr < 10.0)&(slop_Arr > 0),1,0)
    grpr = focalM(slop_grid)
    greenS = np.zeros(slop_grid.shape).astype(float)
    #checking if the percent green is larger than 30%; creates boolean grid of 1 & 0s based on this threshold
    greenS = np.where((grpr > 50.0),1,0).astype(float)
    return greenS

#Aspect (below)
#-------------------------------------------------------------------------------------------------"
def asp_suit(jeff_dem_asp):
    asp_Arr = arcpy.RasterToNumPyArray(jeff_dem_asp)
    asp_Arr[asp_Arr <= 0] = 0
    
    aspect_grid = np.where((asp_Arr > 90.0) & (asp_Arr < 270.0) &(asp_Arr !=0),1,0)
    greenPer = focalM(aspect_grid)
    #greenSuit = focalM(aspect_grid)
    #print focalM(nlcdGreen)
    greenSuit = np.zeros(aspect_grid.shape).astype(float)
    #checking if the percent green is larger than 30%; creates boolean grid of 1 & 0s based on this threshold
    greenSuit = np.where((greenPer > 90.0)&(greenPer !=0),1,0).astype(float)
    return greenSuit

#Putting together NP arrays and creating combined raster
#------------------------------------------------------------------------------------------------------
def np_2_raster(jeff_dem_ras, jeff_dem_slop, greenSuit, greenS, veg_A, slop_Arr):
    llpnt = jeff_dem_ras.extent.lowerLeft
    demSize = jeff_dem_ras.meanCellHeight
    
    allSuit = np.zeros(slop_Arr.shape).astype(float)
    allSuit = greenSuit + greenS + veg_A
    
    print "convert Numpy-array to arcpy-raster"
    suitRaster = arcpy.NumPyArrayToRaster(allSuit,llpnt,demSize,demSize)
    arcpy.DefineProjection_management(suitRaster,jeff_dem_ras.spatialReference)
#    print "Saving the Suitability Raster"
    suitRaster.save('suitOut_90')
    return suitRaster