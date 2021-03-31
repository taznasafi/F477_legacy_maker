import my_paths
from F477_legacy_maker import CoverageMaker, get_path, os


def coverge_service_area(run=False, intersect_any_coverage_fhcs=False,
                         LTE_maker=False, Create_verizon_LTE=False,
                         intersect_LTE_coverage_fhcs=False, cal_area=False):

    #any coverage maker
    intx_any = CoverageMaker.CoverageMaker()
    intx_any.in_gdb_path = os.path.join(intx_any.base_input_folder, '_02B_diss_merge_ANY_June_f477_legacy_provider.gdb')
    intx_any.output_folder = intx_any.base_output_folder
    intx_any.out_gdb_name = '_04_Interset_any_diss_merge_June_f477_legacy_provider'
    intx_any.out_gdb = os.path.join(intx_any.output_folder, intx_any.out_gdb_name + ".gdb")
    intx_any.create_gdb()

    #LTE verizon Coverage intersector
    vrz_LTE = CoverageMaker.CoverageMaker()
    vrz_LTE.in_gdb_path = os.path.join(vrz_LTE.base_input_folder, '_02A_diss_merge_June_f477_legacy_provider.gdb')
    vrz_LTE.in_gdb_2_path = r"D:\Census_Data\US Map\tl_2010_state10_wgs84.gdb"
    vrz_LTE.output_folder = vrz_LTE.base_input_folder
    vrz_LTE.out_gdb_name = '_03_Verizon_LTE_June_f477_legacy_provider'
    vrz_LTE.out_gdb = os.path.join(vrz_LTE.output_folder, vrz_LTE.out_gdb_name + ".gdb")
    vrz_LTE.create_gdb()


    #LTE Coverage intersector
    LTE = CoverageMaker.CoverageMaker()
    LTE.in_gdb_path = os.path.join(LTE.base_input_folder, '_02A_diss_merge_June_f477_legacy_provider.gdb')
    LTE.output_folder = LTE.base_input_folder
    LTE.out_gdb_name = '_03_LTE_June_f477_legacy_provider'
    LTE.out_gdb = os.path.join(LTE.output_folder, LTE.out_gdb_name + ".gdb")
    LTE.create_gdb()


    #LTE Coverage intersector
    intx_LTE = CoverageMaker.CoverageMaker()
    intx_LTE.in_gdb_path = LTE.out_gdb
    intx_LTE.output_folder = intx_LTE.base_output_folder
    intx_LTE.out_gdb_name = '_05_Interset_LTE_merge_June_f477_legacy_provider'
    intx_LTE.out_gdb = os.path.join(intx_LTE.output_folder, intx_LTE.out_gdb_name + ".gdb")
    intx_LTE.create_gdb()

    if run:

        if intersect_any_coverage_fhcs:
            intx_any.intersect_coverage_service_area_fc(suffix="_ANY_COVERAGE")
            if cal_area:
                intx_any.in_gdb_path = intx_any.out_gdb
                intx_any.calculate_pct_area(numerator_col_name="coverage_area_kilometers",
                                            denom_col_name="subsidy_area_by_block", pct_col_name="pct_of_sac_covered")


        if LTE_maker:

            if Create_verizon_LTE:
                vrz_LTE.create_vrz_LTE_by_state()
                vrz_LTE.out_gdb = LTE.out_gdb


            LTE.create_LTE()


        if intersect_LTE_coverage_fhcs:
            intx_LTE.intersect_coverage_service_area_fc(suffix="_LTE_COVERAGE")

            if cal_area:
                intx_LTE.in_gdb_path = intx_LTE.out_gdb
                intx_LTE.calculate_pct_area(numerator_col_name="coverage_area_kilometers",
                                            denom_col_name="subsidy_area_by_block",
                                            pct_col_name="pct_of_sac_covered",
                                            convert_meter_to_km=False)

