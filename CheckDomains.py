import arcpy
import os

input_geodatabases = arcpy.GetParameter(0)

for geodatabase in input_geodatabases:
    env = arcpy.env.workspace = geodatabase
    domains = arcpy.da.ListDomains(geodatabase)
    arcpy.AddMessage('Original Workspace: {0}.'.format(arcpy.env.workspace))
    #arcpy.AddMessage('Domains {0} .'.format(domains))
    datasets = arcpy.ListDatasets()
    #for dataset in datasets:
    #    arcpy.AddMessage('Datasets {0} .'.format(dataset))
    for dataset in datasets:
        path = arcpy.env.workspace = str(env) + "\\" + dataset
        #arcpy.AddMessage('Workspace: {0}.'.format(arcpy.env.workspace))
        feature_classes = arcpy.ListFeatureClasses()
        #arcpy.AddMessage('Feature Classes {0} .'.format(feature_classes))
        for feature_class in feature_classes:
            fields = arcpy.ListFields(feature_class, "*", "All")
            arcpy.AddMessage('Feature class: {0} .'.format(feature_class))
            errors = 0
            for field in fields:
                #arcpy.AddMessage('Field name: {0} .'.format(field.name))
                if field.domain != "":
                    #arcpy.AddMessage('Field domain: {0}.'.format(field.domain))
                    for domain in domains:
                        if field.domain == domain.name:
                            arcpy.AddMessage('Domain found in list. {0}.'.format(field.domain))
                            if domain.domainType == 'CodedValue':
                                arcpy.AddMessage('Domain is Coded {0} .'.format(domain.name))
                                coded_values = domain.codedValues
                                #arcpy.AddMessage('Coded Values: {0} .'.format(coded_values))

                                if arcpy.Exists(feature_class):
                                    arcpy.AddMessage("Feature class Exists")
                                cursor = arcpy.da.SearchCursor(feature_class, ["OID@", field.name])
                                if arcpy.Exists(cursor):
                                    arcpy.AddMessage("Cursor Exists")
                                for f in cursor:
                                    arcpy.AddMessage('Row: {0} .'.format(f[0]))
                                    if f[1] not in coded_values:
                                        arcpy.AddMessage(
                                            'Row {0} has values that are not within the domain.'.format(row[0]))
                                        errors += 1

                            elif domain.domainType == 'Range':
                                arcpy.AddMessage('Domain is Ranged {0} .'.format(domain.name))
                                with arcpy.da.SearchCursor(feature_class, ["OID@", field.name]) as cursor:
                                    for row in cursor:
                                        if not ((row[1] > domain.range[0]) and (row[1] < domain.range[1])):
                                            arcpy.AddMessage(
                                                'Row {0} has values that are not within the domain.'.format(row[0]))
                                            errors += 1
            arcpy.AddMessage('Feature class: {0} has {1} errors found.'.format(feature_class, errors))
        del feature_classes