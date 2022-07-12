import arcpy

dataset = arcpy.GetParameter(0)
input_fields = arcpy.GetParameterAsText(1).split(";")
arcpy.AddMessage('Fields: {0} '.format(input_fields))


#for field in :
    #field_list = arcpy.ListFields(dataset)
    #index = field_list.index(field)
    #desc = arcpy.Describe(field_list[index])
    #if desc.type == "String":
with arcpy.da.UpdateCursor(dataset, input_fields) as cursor:
    for row in cursor:
        if row[0] != None:
            row[0] = row[0].capitalize()
            cursor.updateRow(row)

