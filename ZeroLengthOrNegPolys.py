import arcpy

input_polygons = arcpy.GetParameter(0)
input_polylines = arcpy.GetParameter(1)



for line_layer in input_polylines:
    errors = 0
    with arcpy.da.SearchCursor(line_layer, ["OID@","SHAPE@LENGTH"]) as cursor:
        for f in cursor:
            if f[0] < 0:
                arcpy.AddMessage("{0} has negative polylines. ID Number: {1} has length {2}".format(line_layer, f[0], f[1]))
                errors += 1
            elif f[0] == 0:
                arcpy.AddMessage("{0} has zero length polylines. ID Number: {1} has length {2}".format(line_layer, f[0], f[1]))
                errors += 1

    arcpy.AddMessage("{0} errors were found in dataset {1}".format(errors, line_layer))

for polygon_layer in input_polygons:
    errors = 0
    with arcpy.da.SearchCursor(polygon_layer, ["OID@", "SHAPE@AREA"]) as cursor:
        for f in cursor:
            if f[0] < 0:
                arcpy.AddMessage("{0} has negative polygons. ID Number: {1} has length {2}".format(polygon_layer, f[0], f[1]))
                errors += 1
            elif f[0] == 0:
                arcpy.AddMessage("{0} has zero length polylines. ID Number: {1} has length {2}".format(polygon_layer, f[0], f[1]))
                errors += 1
    arcpy.AddMessage("{0} errors were found in dataset {1}".format(errors, polygon_layer))