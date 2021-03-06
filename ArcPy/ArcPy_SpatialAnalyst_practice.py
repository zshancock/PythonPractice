## Use WellsSubset shapefile to generate a raster using Natural Neighbor interpolation - then use the contour     
## tool with 1500 as interval to generate the contour of resulting raster 

import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = "C:\\Users\\Zac\\Desktop\\Classwork\\GIS 4080\\Lesson3\\Lesson3_Data"
arcpy.CheckOutExtension("Spatial") 

## First: Creating the Natural Neighbor interpolation raster

# Define Local variables.

input_feature = "WellsSubset.shp"
z_field = "TD"

# Run Natural Neighbor and save output.

outNatNbr = NaturalNeighbor(input_feature, z_field)
outNatNbr.save("C:\\Users\\Zac\\Desktop\\Classwork\\GIS 4080\\Lesson3\\Lesson3_Data\\natnbr")


## Second: Using the Contours tool
 
# Set local variables

inRaster = "natnbr"
contourInterval = 1500
outcontour = "C:\\Users\\Zac\\Desktop\\Classwork\\GIS 4080\\Lesson3\\Lesson3_Data\\contour"

# Run Contour tool.

Contour(inRaster, outcontour, contourInterval)

# Check In Extension.

arcpy.CheckInExtension("Spatial") 
