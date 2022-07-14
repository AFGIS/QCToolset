import arcpy

input_rasters = arcpy.GetParameter(0)

for raster in input_rasters:
    arcpy.management.CalculateStatistics(raster)
    minimum_value = arcpy.management.GetRasterProperties(raster, property_type="MINIMUM")
    result = minimum_value.getOutput(0)
    if float(result) < 0:
        arcpy.AddMessage("{0} has negative values".format(raster))