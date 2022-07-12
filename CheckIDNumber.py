import arcpy
import os

input_datasets = arcpy.GetParameter(0)
recalculate = arcpy.GetParameter(1)

arcpy.AddMessage('Recalculate: {0} .'.format(recalculate))

for dataset in input_datasets:
    if arcpy.ListFields(dataset, "FID", "All"):
        field = "FID"
    else:
        field = "OBJECTID"

    value = 1
    prev_value = 0
    errors = 0
    for row in arcpy.da.SearchCursor(dataset, "OID@", sql_clause=(None, 'ORDER BY {0}'.format(field))):
        if row[0] != value:
            arcpy.AddMessage(
                'Dataset: {0} ID Number {1} contains an error. The value of the previous ID is: {2}'.format(dataset, str(row[0]),
                                                                                              prev_value))
            prev_value = value
            value = row[0]+1
            errors += 1
        else:
            prev_value = value
            value += 1

    feature_count = arcpy.management.GetCount(dataset)
    if (str(feature_count) != str(value-1)):
        errors += 1
        arcpy.AddMessage(
            'Dataset: {0} The final ID Number {1} does not match the total feature count of {2}.'.format(dataset, value-1,
                                                                                                         feature_count))
    arcpy.AddMessage('Dataset: {0} has a total of {1} errors found.'.format(dataset, errors))

    if recalculate:
        if errors > 0:
            name = os.path.basename(str(dataset))
            new_dataset = arcpy.conversion.FeatureClassToFeatureClass(dataset, os.path.dirname(str(dataset)), "temp")
            arcpy.management.Delete(dataset)
            arcpy.management.Rename(new_dataset, name)
            arcpy.AddMessage('IDs were recalculated for dataset: {0} .'.format(new_dataset))
