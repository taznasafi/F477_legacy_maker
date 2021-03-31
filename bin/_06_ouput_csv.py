import my_paths
from F477_legacy_maker import CoverageMaker, get_path, os


def output_csv(run=False, type=None):
    csv_maker = CoverageMaker.CoverageMaker()
    csv_maker.output_folder = CoverageMaker.int_paths.output_csv_path
    if run:
        if type == "any":
            csv_maker.in_gdb_path = os.path.join(CoverageMaker.CoverageMaker.base_output_folder,
                                                 '_04_Interset_any_diss_merge_June_f477_legacy_provider.gdb')
            csv_maker.export_csv()
        elif type == 'lte':
            csv_maker.in_gdb_path = os.path.join(CoverageMaker.CoverageMaker.base_output_folder,
                                                 '_05_Interset_LTE_merge_June_f477_legacy_provider.gdb')
            csv_maker.export_csv()
        else:
            print("Specify type either as 'any' or 'lte'")
