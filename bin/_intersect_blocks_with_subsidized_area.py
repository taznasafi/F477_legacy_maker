from F477_legacy_maker import CoverageMaker, os
import my_paths

def create_subsidized_area_by_block(run=False, cal_area=False):

    subsidy = CoverageMaker.CoverageMaker()
    subsidy.in_gdb_path = my_paths.fhcs
    subsidy.in_gdb_2_path = my_paths.block
    subsidy.output_folder = subsidy.base_input_folder
    subsidy.out_gdb_name = "_input_fhcs_by_block"
    subsidy.out_gdb = os.path.join(subsidy.output_folder, subsidy.out_gdb_name+".gdb")
    subsidy.create_gdb()

    if run:

        subsidy.make_fhcs()
        subsidy.in_gdb_path = subsidy.out_gdb
        if cal_area:
                    subsidy.batch_add_field(field_name="subsidy_area_by_block", field_type="DOUBLE")
                    subsidy.batch_calculate_area(field_name='subsidy_area_by_block', expression="!shape.geodesicAREA@SQUAREKILOMETERS!")
