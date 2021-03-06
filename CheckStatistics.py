import arcpy

input_rasters = arcpy.GetParameter(0)
calculate_statistics = arcpy.GetParameter(1)

errors = 0

for raster in input_rasters:
    try:
        mean = arcpy.management.GetRasterProperties(raster, property_type="MEAN")
        result = mean.getOutput(0)

    except:
        errors += 1
        if calculate_statistics == True:
            arcpy.management.CalculateStatistics(raster)
            arcpy.AddMessage("Statistics calculated for {0}.".format(raster))
        else:
            arcpy.AddMessage("{0} does not have statistics calculated.".format(raster))

if errors == 0:
    arcpy.AddMessage("All input rasters have statistics.")
