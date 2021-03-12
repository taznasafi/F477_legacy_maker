from bin import _01_extract_shp_zipfiles, _02_rename_repair_geometry, _03_shp_fc, _04_process_f477_fc, _05_create_any_and_LTE_coverage_service_area, _06_ouput_csv


if __name__ == '__main__':
    _01_extract_shp_zipfiles.extract_zipfiles(run=True, copy_from_k=True)
    _01_extract_shp_zipfiles.extract_zipfiles(run=True, unzip=True)

    _02_rename_repair_geometry.repair_shp(run=True, sanatize_file_names=True)
    _02_rename_repair_geometry.repair_shp(run=True, fix_geom=True)
    _02_rename_repair_geometry.repair_shp(run=True, rename_shp=True)

    _03_shp_fc.shp_to_gdb(run=True)

    _04_process_f477_fc.process_fc(run=True, merger=True)
    _04_process_f477_fc.process_fc(run=True, disovler=True)
    _04_process_f477_fc.process_fc(run=True, tmo_maker=True)
    _04_process_f477_fc.process_fc(run=True, verizon_maker=True)
    _04_process_f477_fc.process_fc(run=True, any_disovler=True)

    _05_create_any_and_LTE_coverage_service_area.coverge_service_area(run=True, intersect_any_coverage=True, cal_area=True)
    _05_create_any_and_LTE_coverage_service_area.coverge_service_area(run=True, LTE_maker=True, Create_verizon_LTE=True)
    _05_create_any_and_LTE_coverage_service_area.coverge_service_area(run=True, LTE_maker=True)
    _05_create_any_and_LTE_coverage_service_area.coverge_service_area(run=True, intersect_LTE_coverage=True, cal_area=True)
    _05_create_any_and_LTE_coverage_service_area.coverge_service_area(run=True, intersect_any_coverage_by_block=True, cal_area=True)
    _05_create_any_and_LTE_coverage_service_area.coverge_service_area(run=True, intersect_LTE_coverage_by_block=True, cal_area=True)

    _06_ouput_csv.output_csv(run=True, type='any')
    _06_ouput_csv.output_csv(run=True, type='lte')



