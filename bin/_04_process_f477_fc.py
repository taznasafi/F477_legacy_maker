import my_paths
from F477_legacy_maker import CoverageMaker, get_path, os


def process_fc(run=False, merger=False, disovler=False, any_disovler=False, tmo_maker=False, verizon_maker=False):

    merge = CoverageMaker.CoverageMaker()
    merge.in_gdb_path = os.path.join(merge.base_input_folder, 'June_f477_legacy_provider.gdb')
    merge.output_folder = merge.base_input_folder
    merge.out_gdb_name = '_01_merge_June_f477_legacy_provider'
    merge.out_gdb = os.path.join(merge.output_folder, merge.out_gdb_name+".gdb")
    merge.create_gdb()

    diss = CoverageMaker.CoverageMaker()
    diss.in_gdb_path = merge.out_gdb
    diss.output_folder = diss.base_input_folder
    diss.out_gdb_name = '_02A_diss_merge_June_f477_legacy_provider'
    diss.out_gdb = os.path.join(diss.output_folder, diss.out_gdb_name + ".gdb")
    diss.create_gdb()

    tmo = CoverageMaker.CoverageMaker()
    tmo.in_gdb_path = diss.out_gdb
    tmo.in_gdb_2_path = r"D:\Census_Data\US Map\tl_2010_state10_wgs84.gdb"
    tmo.output_folder = tmo.base_input_folder
    tmo.out_gdb_name = '_02B_diss_merge_June_f477_legacy_tmo'
    tmo.out_gdb = os.path.join(tmo.output_folder, tmo.out_gdb_name + ".gdb")
    tmo.create_gdb()

    vrz = CoverageMaker.CoverageMaker()
    vrz.in_gdb_path = merge.out_gdb
    vrz.in_gdb_2_path = r"D:\Census_Data\US Map\tl_2010_state10_wgs84.gdb"
    vrz.output_folder = vrz.base_input_folder
    vrz.out_gdb_name = '_02B_diss_merge_June_f477_legacy_verizon'
    vrz.out_gdb = os.path.join(vrz.output_folder, vrz.out_gdb_name + ".gdb")
    vrz.create_gdb()

    diss_any = CoverageMaker.CoverageMaker()
    diss_any.in_gdb_path = diss.out_gdb
    diss_any.output_folder = diss_any.base_input_folder
    diss_any.out_gdb_name = '_02B_diss_merge_ANY_June_f477_legacy_provider'
    diss_any.out_gdb = os.path.join(diss_any.output_folder, diss_any.out_gdb_name + ".gdb")
    diss_any.create_gdb()



    if run:

        if merger:
            merge.merge_fc()

        if disovler:
            print("dissolving")
            diss.dissolve_fc(dissolve_list=['pid', 'pname', 'TECHNOLOGY'])

        if tmo_maker:
            tmo.intersect_by_state_tmo()
            tmo.in_gdb_path = tmo.out_gdb
            tmo.delete_empty_fc()
            tmo.diss_tmo_any_coverage_by_state(dissolve_list=['pid', 'pname'])
            tmo.in_gdb_path = tmo.out_gdb
            tmo.out_gdb = diss_any.out_gdb
            tmo.merge_any_tmo_coverage_export()


        if verizon_maker:
            # intersect by state
            vrz.intersect_by_state_verizon() # intersect the verizon parts with state boundary
            vrz.in_gdb_path = vrz.out_gdb # declare input gdb same as it self
            vrz.delete_empty_fc() # delete empty fc from input gdb

            #any coverage
            vrz.in_gdb_path = vrz.out_gdb
            vrz.out_gdb = diss_any.out_gdb
            vrz.create_any_coverage()

            #dissovle coveages by tech
            vrz.out_gdb = diss.out_gdb
            vrz.in_gdb_path = os.path.join(vrz.output_folder, vrz.out_gdb_name + ".gdb")
            vrz.create_tech_coverage()



        if any_disovler:
            diss_any.in_gdb_path = diss.out_gdb
            diss_any.dissolve_fc(dissolve_list=['pid', 'pname'])

