from F477_legacy_maker import CoverageMaker


def repair_shp(run=False, sanatize_file_names=False, rename_shp=False):
    if run:

        repair = CoverageMaker.CoverageMaker()

        if rename_shp:
            repair.rename_shp_name()

        if sanatize_file_names:
            print("sanatizing_shp")
            repair.repair_shape_file_name()