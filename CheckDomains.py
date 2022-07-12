import arcpy

input_geodatabases = arcpy.GetParameter(0)

for geodatabase in input_geodatabases:
    arcpy.env.workspace = geodatabase
    domains = arcpy.da.ListDomains(geodatabase)
    #arcpy.AddMessage('Domains {0} .'.format(domains))
    datasets = arcpy.ListFeatureClasses("*", "All")
    #arcpy.AddMessage('Datasets {0} .'.format(datasets))

    for dataset in datasets:
        fields = arcpy.ListFields(dataset, "*", "All")
        #arcpy.AddMessage('Fields {0} .'.format(fields))
        errors = 0
        for field in fields:
            #arcpy.AddMessage('Domains {0} .'.format(field.domain))
            if field.domain is not None:
                arcpy.AddMessage('Field {0}.'.format(field.domain))
                if field.domain in domains:
                    #arcpy.AddMessage('Field {0}.'.format(field.name))
                    index = domains.index(field.domain)
                    arcpy.AddMessage('Domain {0} for field {1}.'.format(domains[index].name, field))
                    if domains[index].domainType == 'CodedValue':
                        coded_values = domains[index].codedValues
                        with arcpy.da.SearchCursor(dataset, ["OID@", field]) as cursor:

                            for row in cursor:
                                arcpy.AddMessage('Row {0} .'.format(row[1]))
                                if row[1] not in coded_values:
                                    arcpy.AddMessage(
                                        'Row {0} has values that are not within the domain.'.format(row[0]))
                                    errors += 1


                    elif domains[index].domainType == 'Range':
                        with arcpy.da.SearchCursor(dataset, ["OID@", field]) as cursor:
                            for row in cursor:
                                if not ((row[1] > domains[index].range[0]) and (row[1] < domains[index].range[1])):
                                    arcpy.AddMessage('Row {0} has values that are not within the domain.'.format(row[0]))
                                    errors += 1
        desc = arcpy.Describe(dataset)
        arcpy.AddMessage('Dataset {0} has {1} errors found.'.format(desc.name, errors))