import arcpy

input_rasters = arcpy.GetParameter(0)
input_spatial_ref = arcpy.GetParameter(1)
errors = False

for raster in input_rasters:
    spatial_ref = arcpy.Describe(raster).spatialReference
    if spatial_ref.name == "Unknown":
        errors = True
        arcpy.AddMessage("{0} has an unknown spatial reference".format(raster))
    elif spatial_ref != input_spatial_ref:
        arcpy.AddMessage("{0} has the spatial reference {1}".format(raster, spatial_ref.name))
        errors = True

if errors == False:
    arcpy.AddMessage("No Errors Found.")



