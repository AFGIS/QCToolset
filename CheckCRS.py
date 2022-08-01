import arcpy

input_layers = arcpy.GetParameter(0)
input_spatial_ref = arcpy.GetParameter(1)
errors = False



for layer in input_layers:
    spatial_ref = arcpy.Describe(layer).spatialReference
    ref1 = str(spatial_ref.name).strip()
    ref2 = str(input_spatial_ref.name).strip()
    if spatial_ref.name == "Unknown":
        errors = True
        arcpy.AddMessage("{0} has an unknown spatial reference".format(layer))
        continue
    elif ref1 != ref2:
       arcpy.AddMessage("{0} has the spatial reference {1} default value is {2}".format(layer, spatial_ref.name,
                                                                                         input_spatial_ref.name))
       errors = True

if errors == False:
    arcpy.AddMessage("No Errors Found.")



