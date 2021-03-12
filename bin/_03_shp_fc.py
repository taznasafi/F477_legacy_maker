import my_paths
from F477_legacy_maker import CoverageMaker, get_path
import os

def shp_to_gdb(run=False):

    trans = CoverageMaker.CoverageMaker()
    trans.output_folder = trans.base_input_folder
    trans.out_gdb_name = 'June_f477_legacy_provider'
    trans.out_gdb = os.path.join(trans.output_folder, trans.out_gdb_name+".gdb")
    trans.create_gdb()

    if run:
        trans.shp_to_fc()