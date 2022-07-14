import arcpy

dataset = arcpy.GetParameter(0)
input_fields = arcpy.GetParameterAsText(1).split(";")
arcpy.AddMessage('Fields: {0} '.format(input_fields))
sentence_case = arcpy.GetParameter(2)
remove_spaces = arcpy.GetParameter(3)




with arcpy.da.UpdateCursor(dataset, input_fields) as cursor:
    for row in cursor:
        for i in range(0, len(input_fields)):
            if row[i] != None:
                if sentence_case:
                    row[i] = row[i].capitalize()
                if remove_spaces:
                    row[i] = row[i].strip()
                cursor.updateRow(row)

