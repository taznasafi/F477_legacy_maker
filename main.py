from bin import _01_extract_shp_zipfiles, _02_rename_repair_geometry, _03_shp_fc, _04_process_f477_fc, _05_create_any_and_LTE_coverage_service_area, _06_ouput_csv
from bin import _intersect_blocks_with_subsidized_area

if __name__ == '__main__':
    _01_extract_shp_zipfiles.extract_zipfiles(run=False, copy_from_k=True)
    _01_extract_shp_zipfiles.extract_zipfiles(run=False, unzip=True)
    _02_rename_repair_geometry.repair_shp(run=False, sanatize_file_names=True) #todo: some how fix name so that when renameing ladf.lsdf.shp can be renamed correctly, right now it is done manually
    _02_rename_repair_geometry.repair_shp(run=False, rename_shp=True)
    _02_rename_repair_geometry.repair_shp(run=False, sanatize_file_names=True)

    _03_shp_fc.shp_to_gdb(run=False, repair_geom=True)

    _04_process_f477_fc.process_fc(run=False, merger=True)
    _04_process_f477_fc.process_fc(run=False, disovler=True)
    _04_process_f477_fc.process_fc(run=False, tmo_maker=True)
    _04_process_f477_fc.process_fc(run=False, verizon_maker=True)
    _04_process_f477_fc.process_fc(run=False, any_disovler=True)

    #create subsidy area by block
    _intersect_blocks_with_subsidized_area.create_subsidized_area_by_block(run=False, cal_area=True)

    # Intersect the coverage by cetc state subsidized coverage
    _05_create_any_and_LTE_coverage_service_area.coverge_service_area(run=True, intersect_any_coverage_fhcs=True, cal_area=True)
    _05_create_any_and_LTE_coverage_service_area.coverge_service_area(run=True, LTE_maker=True)
    _05_create_any_and_LTE_coverage_service_area.coverge_service_area(run=True, intersect_LTE_coverage_fhcs=True, cal_area=True)



    _06_ouput_csv.output_csv(run=True, type='any')
    _06_ouput_csv.output_csv(run=True, type='lte')
