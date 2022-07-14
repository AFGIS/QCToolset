import arcpy

contours = arcpy.GetParameter(0)
check_z_populated = arcpy.GetParameter(1)
check_z_positive = arcpy.GetParameter(2)
check_m_populated = arcpy.GetParameter(3)

def check_z_positive(dataset):
    desc = arcpy.Describe(dataset)
    if desc.hasZ:
        errors = 0
        with arcpy.da.SearchCursor(dataset, ["OID@", "SHAPE@Z"]) as cursor:
            for f in cursor:
                if f[1] <= 0:
                    arcpy.AddMessage("{0} has the value {1} for ID {2}, which is equal to or less than zero (0)."
                                     .format(dataset, f[1], f[0]))
                    errors += 1
        if errors == 0:
            arcpy.AddMessage("All Z-values for dataset {0} are positive.".format(dataset))
    else:
        arcpy.AddMessage("{0} does not have Z-values enabled.".format(dataset))

def check_z_populated(dataset):
    desc = arcpy.Describe(dataset)
    if desc.hasZ:
        all_rows = [i[0] for i in arcpy.da.SearchCursor(dataset, ["SHAPE@Z"])]
        if not all_rows:
            arcpy.AddMessage("{0} has Z-values enabled, but they are not populated.".format(dataset))
        elif (max(all_rows) != 0) and (min(all_rows) != 0):
            arcpy.AddMessage("{0} has populated Z-values.".format(dataset))
        else:
            arcpy.AddMessage("{0} has Z-values enabled, but they are not populated.".format(dataset))
    else:
        arcpy.AddMessage("{0} does not have Z-values enabled.".format(dataset))

def check_m_populated(dataset):
    desc = arcpy.Describe(dataset)
    if desc.hasM:
        all_rows = [i[0] for i in arcpy.da.SearchCursor(dataset, ["SHAPE@M"])]
        if not all_rows:
            arcpy.AddMessage("{0} has M-values enabled, but they are not populated.".format(dataset))
        elif (max(all_rows) != 0) and (min(all_rows) != 0):
            arcpy.AddMessage("{0} has populated M-values.".format(dataset))
        else:
            arcpy.AddMessage("{0} has M-values enabled, but they are not populated.".format(dataset))
    else:
        arcpy.AddMessage("{0} does not have M-values enabled.".format(dataset))

for contour in contours:

    if check_z_positive:
        check_z_positive(contour)

    if check_z_populated:
        check_z_populated(contour)

    if check_m_populated:
        check_m_populated(contour)

