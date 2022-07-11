import arcpy

input_vectors = arcpy.GetParameter(0)

for vector in input_vectors:
    errors = 0
    with arcpy.da.UpdateCursor(vector, "*") as cursor:
        for row in cursor:
            for i in range(len(row)):
                if not row[i] or (str(row[i]).lower() == "n/a") or (str(row[i]).lower() == "na") or \
                        (str(row[i]).isdigit() == "0") or (str(row[i]).replace(" ", "") == ""):
                    row[i] = None
                    cursor.updateRow(row)
                    errors += 1
    arcpy.AddMessage("{0} n/a or missing values were corrected in dataset {1}".format(errors, vector))