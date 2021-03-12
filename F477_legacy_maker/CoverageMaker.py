import arcpy
import os
import pandas as pd
from F477_legacy_maker import logger, get_path
import my_paths
from collections import defaultdict
import F477_legacy_maker.__init__ as int_paths
import re


class CoverageMaker:
    base_input_folder, base_output_folder = int_paths.input_path, int_paths.output_path
    gdb_output_dic = defaultdict(list)

    def __init__(self, in_gdb_path=None, in_gdb_2_path=None, in_path=None,
                 output_folder=None, generic_out_path=None,
                 out_gdb_name=None, out_gdb=None):
        self.in_gdb_path = in_gdb_path
        self.in_gdb_2_path = in_gdb_2_path
        self.in_path = in_path
        self.output_folder = output_folder
        self.generic_out_path = generic_out_path
        self.out_gdb_name = out_gdb_name
        self.out_gdb = out_gdb

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def create_gdb(self):
        """
        creates ESRI GDB, given that you have provided Class properties correctly.
        """

        if not arcpy.Exists(self.out_gdb):

            arcpy.CreateFileGDB_management(out_folder_path=self.output_folder, out_name=self.out_gdb_name)
            # print(arcpy.GetMessages(0))
        else:
            print("GDB Exists")

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def add_field(self, in_fc, field_name, field_type):
        """

        :param in_fc: input featureclass
        :param field_name: the name of a field
        :param field_type: type of field [string, double, short, long, date]
        """
        # check if the field exits
        fields = len(arcpy.ListFields(dataset=in_fc, wild_card=field_name))
        try:

            if fields < 1:
                # if the length of the field is less than 1 then create a field with specified params
                arcpy.AddField_management(in_table=in_fc, field_name=field_name, field_type=field_type)
                # print(arcpy.GetMessages(0))
        except:
            raise '{} field exits'.format(field_name)

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def calculate_field(self, in_fc, in_field, expression):
        """
        Calculate field based on Python expression
        :param in_fc: input featureclass
        :param in_field: input field
        :param expression: python expression (i.e. !shape.geodesiclength@meters!)
        """
        # print('calculating field, please wait')
        arcpy.CalculateField_management(in_table=in_fc, field=in_field, expression=expression)
        # print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def repair_geom(self):

        shp_dic = get_path.pathFinder.get_shapefile_path_walk_dict(int_paths.zipfolder_path)
        # print(shp_dic)
        error_file = {}
        for basepath, shp in shp_dic.items():
            print(shp)
            try:

                arcpy.RepairGeometry_management(in_features=os.path.join(basepath, shp[0]))
                print(arcpy.GetMessages(0))

            except:

                print("there was some kind of error")
                print(arcpy.GetMessages())
                error_file[os.path.join(basepath, shp[0])] = [print(arcpy.GetMessages())]
        pd.DataFrame.from_dict(error_file,).to_csv(os.path.join(int_paths.output_path,
                                                               'shapefile_cannot_be_repairted.csv'))

    @classmethod
    def filename_replacer(cls, file_name):
        path, fname = os.path.split(file_name)
        print(fname)
        regex = r"(\.)(?!(\.*shp))"
        test_str = fname
        subst = "_"
        # You can manually specify the number of replacements by changing the 4th argument
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        if result:
            return os.path.join(path, result)
        else:
            return os.path.join(path, fname)

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def repair_zip_name(self):
        print('repairing shp names')
        shp_dic = get_path.pathFinder.get_shapefile_path_walk_dict(int_paths.zipfolder_path)
        # print(shp_dic)

        for basepath, shp in shp_dic.items():
            input_path = os.path.join(basepath, shp[0])
            output_path = CoverageMaker.filename_replacer(os.path.join(basepath, shp[0]))
            if input_path != output_path:
                arcpy.Rename_management(input_path, out_data=output_path)
                print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def rename_shp_name(self):

        shp_dict = get_path.pathFinder.get_shapefile_path_walk_dict(int_paths.zipfolder_path)

        for base, shp in shp_dict.items():
            print(shp)

            name_dict = re.search(pattern=r"__(?P<pid>\d{1,3})_(?P<pname>\w.+)__(?P<lastbit>F477_(\d{5,7}))(?:\\)",
                                 string=os.path.join(base, shp[0])).groupdict()
            print(name_dict)

            output_path = os.path.join(base, "__{}_{}__{}.shp".format(name_dict['pid'],
                                                                      name_dict['pname'],
                                                                      name_dict['lastbit']))
            if os.path.join(base, shp[0]) != output_path:
                arcpy.Rename_management(in_data=os.path.join(base, shp[0]),
                                        out_data=output_path)
                print(arcpy.GetMessages())

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def shp_to_fc(self):
        shp_dict = get_path.pathFinder.get_shapefile_path_walk_dict(int_paths.zipfolder_path)
        for base, shp in shp_dict.items():
            print(shp)
            output = os.path.join(self.out_gdb, os.path.join(shp[0].strip(".shp")))
            print(output)
            if not arcpy.Exists(output):
                arcpy.FeatureClassToGeodatabase_conversion(Input_Features=os.path.join(base, shp[0]),
                                                           Output_Geodatabase=self.out_gdb)
                print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def merge_fc(self):

        fc_list = get_path.pathFinder(env=self.in_gdb_path).get_path_for_all_feature_from_gdb()

        fc_pid_wildcard_dict = {}

        for fc in fc_list:
            print(fc)
            name_dict = re.search(
                pattern=r'__(?P<pid>\d{1,3})_(?P<pname>\w.+)__(\w.+)$',
                string=fc).groupdict()

            fc_pid_wildcard_dict[name_dict['pid']] = name_dict['pname']

            CoverageMaker.add_field(self, in_fc=fc, field_name='pid', field_type='LONG')
            CoverageMaker.add_field(self, in_fc=fc, field_name='pname', field_type='TEXT')
            CoverageMaker.calculate_field(self, in_fc=fc , in_field='pid', expression="'{}'".format(name_dict['pid']))
            CoverageMaker.calculate_field(self, in_fc=fc , in_field='pname', expression="'{}'".format(name_dict['pname']))

        for pid, pname in fc_pid_wildcard_dict.items():



            merge_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(fc_list,
                                                                                             "*__{}_*".format(pid))
            if len(merge_list) > 20:

                merge_list_p1 = merge_list[:20]


                fm_dba = arcpy.FieldMap()  # DBA
                fm_pid = arcpy.FieldMap()  # pid
                fm_pname = arcpy.FieldMap()  # pnam
                fm_tech = arcpy.FieldMap()  # tech
                fms = arcpy.FieldMappings()

                # DBA
                for in_file in merge_list_p1:
                    for field in arcpy.ListFields(in_file, "DBA"):
                        fm_dba.addInputField(in_file, field.name)
                # pid
                for in_file in merge_list_p1:
                    for field in arcpy.ListFields(in_file, "pid"):
                        fm_pid.addInputField(in_file, field.name)

                # pname
                for in_file in merge_list_p1:
                    for field in arcpy.ListFields(in_file, "pname"):
                        fm_pname.addInputField(in_file, field.name)

                # tech
                for in_file in merge_list_p1:
                    for field in arcpy.ListFields(in_file, "TECHNOLOGY"):
                        fm_tech.addInputField(in_file, field.name)



                # DBA
                fm_dba.mergeRule = "First"
                f_name = fm_dba.outputField
                f_name.name = 'DBA'
                f_name.length = 255
                f_name.type = "Text"
                fm_dba.outputField = f_name
                fms.addFieldMap(fm_dba)

                # pid
                fm_pid.mergeRule = "First"
                f_name = fm_pid.outputField
                f_name.name = 'pid'
                f_name.type = "LONG"
                fm_pid.outputField = f_name
                fms.addFieldMap(fm_pid)

                # DBA
                fm_pname.mergeRule = "First"
                f_name = fm_pname.outputField
                f_name.name = 'pname'
                f_name.length = 255
                f_name.type = "Text"
                fm_pname.outputField = f_name
                fms.addFieldMap(fm_pname)

                # tech
                fm_tech.mergeRule = "First"
                f_name = fm_pid.outputField
                f_name.name = 'TECHNOLOGY'
                f_name.type = "LONG"
                fm_tech.outputField = f_name
                fms.addFieldMap(fm_tech)

                output = os.path.join(self.out_gdb, "June_2020_F477_{}_{}_merged_p1".format(pid, pname))

                if not arcpy.Exists(output):
                    arcpy.Merge_management(merge_list_p1, output=output, field_mappings=fms)
                    print(arcpy.GetMessages(0))

                merge_list_p2 = merge_list[20:]
                fm_dba = arcpy.FieldMap()  # DBA
                fm_pid = arcpy.FieldMap()  # pid
                fm_pname = arcpy.FieldMap()  # pname
                fm_tech = arcpy.FieldMap()  # tech
                fms = arcpy.FieldMappings()

                # DBA
                for in_file in merge_list_p2:
                    for field in arcpy.ListFields(in_file, "DBA"):
                        fm_dba.addInputField(in_file, field.name)
                # pid
                for in_file in merge_list_p2:
                    for field in arcpy.ListFields(in_file, "pid"):
                        fm_pid.addInputField(in_file, field.name)

                # pname
                for in_file in merge_list_p2:
                    for field in arcpy.ListFields(in_file, "pname"):
                        fm_pname.addInputField(in_file, field.name)

                # tech
                for in_file in merge_list_p2:
                    for field in arcpy.ListFields(in_file, "TECHNOLOGY"):
                        fm_tech.addInputField(in_file, field.name)

                # DBA
                fm_dba.mergeRule = "First"
                f_name = fm_dba.outputField
                f_name.name = 'DBA'
                f_name.length = 255
                f_name.type = "Text"
                fm_dba.outputField = f_name
                fms.addFieldMap(fm_dba)

                # pid
                fm_pid.mergeRule = "First"
                f_name = fm_pid.outputField
                f_name.name = 'pid'
                f_name.type = "LONG"
                fm_pid.outputField = f_name
                fms.addFieldMap(fm_pid)

                # DBA
                fm_pname.mergeRule = "First"
                f_name = fm_pname.outputField
                f_name.name = 'pname'
                f_name.length = 255
                f_name.type = "Text"
                fm_pname.outputField = f_name
                fms.addFieldMap(fm_pname)

                # tech
                fm_tech.mergeRule = "First"
                f_name = fm_tech.outputField
                f_name.name = 'TECHNOLOGY'
                f_name.type = "LONG"
                fm_tech.outputField = f_name
                fms.addFieldMap(fm_tech)

                output = os.path.join(self.out_gdb, "June_2020_F477_{}_{}_merged_p2".format(pid, pname))

                if not arcpy.Exists(output):
                    arcpy.Merge_management(merge_list_p2, output=output, field_mappings=fms)
                    print(arcpy.GetMessages(0))

            else:


                fm_dba = arcpy.FieldMap()  # DBA
                fm_pid = arcpy.FieldMap()  # pid
                fm_pname = arcpy.FieldMap()  # pnam
                fm_tech = arcpy.FieldMap()  # tech
                fms = arcpy.FieldMappings()

                # DBA
                for in_file in merge_list:
                    for field in arcpy.ListFields(in_file, "DBA"):
                        fm_dba.addInputField(in_file, field.name)
                # pid
                for in_file in merge_list:
                    for field in arcpy.ListFields(in_file, "pid"):
                        fm_pid.addInputField(in_file, field.name)

                # pname
                for in_file in merge_list:
                    for field in arcpy.ListFields(in_file, "pname"):
                        fm_pname.addInputField(in_file, field.name)

                # tech
                for in_file in merge_list:
                    for field in arcpy.ListFields(in_file, "TECHNOLOGY"):
                        fm_tech.addInputField(in_file, field.name)

                # DBA
                fm_dba.mergeRule = "First"
                f_name = fm_dba.outputField
                f_name.name = 'DBA'
                f_name.length = 255
                f_name.type = "Text"
                fm_dba.outputField = f_name
                fms.addFieldMap(fm_dba)

                # pid
                fm_pid.mergeRule = "First"
                f_name = fm_pid.outputField
                f_name.name = 'pid'
                f_name.type = "LONG"
                fm_pid.outputField = f_name
                fms.addFieldMap(fm_pid)

                # DBA
                fm_pname.mergeRule = "First"
                f_name = fm_pname.outputField
                f_name.name = 'pname'
                f_name.length = 255
                f_name.type = "Text"
                fm_pname.outputField = f_name
                fms.addFieldMap(fm_pname)

                # tech
                fm_tech.mergeRule = "First"
                f_name = fm_tech.outputField
                f_name.name = 'TECHNOLOGY'
                f_name.type = "LONG"
                fm_tech.outputField = f_name
                fms.addFieldMap(fm_tech)



                output = os.path.join(self.out_gdb, "June_2020_F477_{}_{}_merged".format(pid, pname))

                if not arcpy.Exists(output):
                    arcpy.Merge_management(merge_list, output=output, field_mappings=fms)
                    print(arcpy.GetMessages(0))


    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def dissolve_fc(self, dissolve_list, wildcard=None):

        if wildcard is None:
            fc_list = get_path.pathFinder(env=self.in_gdb_path).get_path_for_all_feature_from_gdb()
        else:
            fc_list = get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb(wildcard=wildcard)

        for fc in fc_list:
            print(fc)

            if os.path.basename(fc) == "June_2020_F477_70_Verizon_Wireless_merged_p1":
                pass
            elif os.path.basename(fc) == "June_2020_F477_70_Verizon_Wireless_merged_p2":
                pass
            elif os.path.basename(fc) == "June_2020_F477_70_Verizon_Wireless_merged__p1_p2_by_tech_dissolved":
                pass
            else:

                output = os.path.join(self.out_gdb, os.path.basename(fc) + '_dissolved')
                print(output)
                if not arcpy.Exists(output):
                    arcpy.PairwiseDissolve_analysis(in_features=fc, out_feature_class=output, dissolve_field=dissolve_list)
                    print(output)



    def delete_empty_fc(self):
        fc_list = get_path.pathFinder(env=self.in_gdb_path).get_path_for_all_feature_from_gdb()

        for fc in fc_list:

            count = str(int(arcpy.GetCount_management(fc).getOutput(0)))
            if count == "0":
                arcpy.Delete_management(fc)

    #tmo
    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def intersect_by_state_tmo(self):

        state_fc_list = get_path.pathFinder(env=self.in_gdb_2_path).get_path_for_all_feature_from_gdb()
        fc_list = get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb(wildcard="*_65_*")

        for state in get_path.pathFinder.make_fips_list():
            print(state)
            state_fc = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(state_fc_list,
                                                                                           "*_{}_*".format(state))
            if len(state_fc) != 0:
                for fc in fc_list:

                    output = os.path.join(self.out_gdb, os.path.basename(fc) + "_" + state)

                    if not arcpy.Exists(output):
                        arcpy.PairwiseIntersect_analysis(in_features=[state_fc[0], fc], out_feature_class=output)
                        print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def diss_tmo_any_coverage_by_state(self, dissolve_list =""):

        state_list = get_path.pathFinder.make_fips_list()
        for state in state_list:

            fc_list = get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb(wildcard="*_{}".format(state))
            if len(fc_list) !=0:

                for fc in fc_list:
                    print(fc)

                    output = os.path.join(self.out_gdb, os.path.basename(fc) + '_dissolved')
                    if not arcpy.Exists(output):
                        arcpy.PairwiseDissolve_analysis(in_features=fc, out_feature_class=output,
                                                        dissolve_field=dissolve_list)
                        print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def merge_any_tmo_coverage_export(self):

        fc_list_p1 = get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb(wildcard="*_dissolved")


        output = os.path.join(self.out_gdb, "June_2020_F477_65_T_Mobile_merged_dissolved_dissolved")
        if not arcpy.Exists(output):
            arcpy.Merge_management(inputs=fc_list_p1, output="in_memory/temp_merge")

            arcpy.PairwiseDissolve_analysis(in_features="in_memory/temp_merge", out_feature_class=output,dissolve_field=["pid", 'pname'])
            print(arcpy.GetMessages(0))


    #verizon

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def intersect_by_state_verizon(self):

        state_fc_list = get_path.pathFinder(env=self.in_gdb_2_path).get_path_for_all_feature_from_gdb()
        fc_list = get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb(wildcard="*_70_*")

        for state in get_path.pathFinder.make_fips_list():
            print(state)
            state_fc = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(state_fc_list,
                                                                                           "*_{}_*".format(state))
            if len(state_fc) != 0:
                for fc in fc_list:

                    output = os.path.join(self.out_gdb, os.path.basename(fc) + "_" + state)

                    if not arcpy.Exists(output):
                        arcpy.PairwiseIntersect_analysis(in_features=[state_fc[0], fc], out_feature_class=output)
                        print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def diss_vrz_coverage_by_state(self, dissolve_list ="", postfix = '_dissolved'):

        state_list = get_path.pathFinder.make_fips_list()
        for state in state_list:

            fc_list = get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb(wildcard="*_{}".format(state))
            if len(fc_list) !=0:

                for fc in fc_list:
                    print(fc)

                    output = os.path.join(self.out_gdb, os.path.basename(fc) + postfix)
                    if not arcpy.Exists(output):
                        arcpy.PairwiseDissolve_analysis(in_features=fc, out_feature_class=output,
                                                        dissolve_field=dissolve_list)
                        print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def merge_any_verizon_coverage(self, wildcard ="*p*_*_dissolved",  out_fc_name = None):

        fc_list_p1 = get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb(wildcard=wildcard)


        output = os.path.join(self.out_gdb, out_fc_name)
        if not arcpy.Exists(output):
            arcpy.Merge_management(inputs=fc_list_p1, output=output)
            print(arcpy.GetMessages(0))

        # #p2
        # fc_list_p2 = get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb(
        #     wildcard="*p2_*_dissolved")
        # output = os.path.join(self.out_gdb, "June_2020_F477_70_Verizon_Wireless_merged_p2_dissolved_dissovled")
        # if not arcpy.Exists(output):
        #     arcpy.Merge_management(inputs=fc_list_p2, output=output)
        #     print(arcpy.GetMessages(0))





    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def intersect_coverage_service_area_fc(self):

        fc_list = get_path.pathFinder(env=self.in_gdb_path).get_path_for_all_feature_from_gdb()
        service_area_list = get_path.pathFinder(env=my_paths.fhcs).get_path_for_all_feature_from_gdb()

        for fc in fc_list:
            print(fc)

            name_dict = re.search(
                pattern=r'(\w.+)_(?P<pid>\d{1,3})_(?P<pname>\w.+)',
                string=fc).groupdict()

            wildcard_fc = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(path_link_list=service_area_list,
                                                                                           wildcard="fhcs_us_{}_*".format(name_dict['pid']))
            for wfc in wildcard_fc:


                output = os.path.join(self.out_gdb, os.path.basename(wfc) + '_service_area_intersect')
                if not arcpy.Exists(output):
                    arcpy.PairwiseIntersect_analysis(in_features=[fc, wfc], out_feature_class=output)
                    print(arcpy.GetMessages())


    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def create_vrz_LTE_by_state(self):

        vrz_parts = get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb("*_70_*_p*_*")
        vrz_temp_lte_fc = []
        for parts in vrz_parts:
            print(parts)
            vrz_temp_lte_fc.append(os.path.basename(parts))
            arcpy.MakeFeatureLayer_management(parts, os.path.basename(parts), """"TECHNOLOGY"=83""")

        #merge the vrz lte parts
        arcpy.Merge_management(inputs=vrz_temp_lte_fc, output='in_memory/temp_merge')
        print(arcpy.GetMessages())

        state_boundary_fc_list = get_path.pathFinder(env=self.in_gdb_2_path).get_path_for_all_feature_from_gdb()

        state_fips = get_path.pathFinder.make_fips_list()

        for state in state_fips:
            output = os.path.join(self.out_gdb, "June_2020_F477_70_Verizon_Wireless_LTE_{}".format(state))

            state_fc = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(state_boundary_fc_list,
                                                                                           wildcard="*_{}_*".format(state))

            if len(state_fc) > 0:

                if not arcpy.Exists(output):
                    arcpy.PairwiseIntersect_analysis(in_features=[state_fc[0],'in_memory/temp_merge'],
                                                     out_feature_class=output)
                    print(arcpy.GetMessages())



    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def export_vrz_lte(self):

        vrz_dissolves= get_path.pathFinder(env=self.in_gdb_path).get_file_path_with_wildcard_from_gdb("*")

        output = os.path.join(self.out_gdb, "June_2020_F477_70_Verizon_Wireless_merged_dissolved_LTE")

        if not arcpy.Exists(output):
            arcpy.Merge_management(inputs=vrz_dissolves, output=output)
            print(arcpy.GetMessages())


    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def create_LTE(self):

        fc_list = get_path.pathFinder(env=self.in_gdb_path).get_path_for_all_feature_from_gdb()

        for fc in fc_list:
            print(fc)
            if os.path.basename(fc) == "June_2020_F477_70_Verizon_Wireless_merged_dissolved_LTE":
                pass
            else:

                lte = arcpy.MakeFeatureLayer_management(fc, 'temp', """"TECHNOLOGY"=83""")

                output = os.path.join(self.out_gdb, os.path.basename(fc)+"_LTE")

                if not arcpy.Exists(output):
                    arcpy.CopyFeatures_management(in_features=lte, out_feature_class=output)
                    print(arcpy.GetMessages())
                    arcpy.Delete_management('temp')
                else:
                    arcpy.Delete_management('temp')

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def calculate_pct_area(self, numerator_col_name = None, denom_col_name=None, pct_col_name=None, convert_meter_to_km=False):

        fc_list = get_path.pathFinder(env=self.in_gdb_path).get_path_for_all_feature_from_gdb()

        for fc in fc_list:
            print(fc)
            CoverageMaker.add_field(self, fc, numerator_col_name, 'DOUBLE')
            CoverageMaker.add_field(self, fc, pct_col_name, 'DOUBLE')
            CoverageMaker.calculate_field(self, fc, numerator_col_name, "!shape.geodesicarea@squarekilometers!")
            if convert_meter_to_km is False:
               CoverageMaker.calculate_field(self, fc, pct_col_name, '!{}!/!{}!'.format(numerator_col_name, denom_col_name))
            if convert_meter_to_km is True:
                CoverageMaker.calculate_field(self, fc, pct_col_name,
                                              '!{}!/(!{}!/1000000)'.format(numerator_col_name, denom_col_name))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def intersect_block(self, wildcard, post_fix):

        fc_list = get_path.pathFinder(env=self.in_gdb_path).get_path_for_all_feature_from_gdb()
        block_list = get_path.pathFinder(env=self.in_gdb_2_path).get_file_path_with_wildcard_from_gdb(wildcard=wildcard)

        for fc in fc_list:
            print(fc)
            for block in block_list:
                print(block)

                output = os.path.join(self.out_gdb, os.path.basename(fc)+"{}".format(post_fix))

                if not arcpy.Exists(output):
                    arcpy.PairwiseIntersect_analysis(in_features=[block, fc],out_feature_class=output)
                    print(arcpy.GetMessages())

    def export_csv(self):
        import csv
        fc_list = get_path.pathFinder(env=self.in_gdb_path).get_path_for_all_feature_from_gdb()

        for fc in fc_list:
            print("exporting {}".format(fc))
            output = os.path.join(self.output_folder, os.path.basename(fc)+".csv")

            not_include_fields = []
            fid_fields = arcpy.ListFields(fc, wild_card="FID*")
            not_include_fields.extend([field.name for field in fid_fields])
            not_include_fields.extend(['Shape', 'Shape_Length', 'Shape_Area'])
            # print(not_include_fields)

            fields = arcpy.ListFields(fc)
            field_names = [field.name for field in fields if field.name not in not_include_fields]

            # print(field_names)

            with open(output, 'w', newline= '') as csvfile:
                w = csv.writer(csvfile)
                w.writerow(field_names)
                with arcpy.da.SearchCursor(fc, field_names=field_names) as c:
                    for row in c:
                        w.writerow(row)
