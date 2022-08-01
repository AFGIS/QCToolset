import arcpy

apply_to_all = arcpy.GetParameter(0)
dataset = arcpy.GetParameter(1)

if apply_to_all:
    input_fields =[f.name for f in arcpy.ListFields(dataset)]
else:
    input_fields = arcpy.GetParameterAsText(2).split(";")
arcpy.AddMessage('Fields: {0} '.format(input_fields))
sentence_case = arcpy.GetParameter(3)
remove_spaces = arcpy.GetParameter(4)




with arcpy.da.UpdateCursor(dataset, input_fields) as cursor:
    for row in cursor:
        for i in range(0, len(input_fields)):
            if row[i] != None:
                if sentence_case:
                    row[i] = row[i].capitalize()
                if remove_spaces:
                    row[i] = row[i].strip()
                cursor.updateRow(row)

