from F477_legacy_maker import CoverageMaker


def repair_shp(run=False, fix_geom=False, sanatize_file_names=False, rename_shp=False):
    if run:

        repair = CoverageMaker.CoverageMaker()

        if sanatize_file_names:
            repair.repair_zip_name()

        if fix_geom:
            repair.repair_geom()

        if rename_shp:
            repair.rename_shp_name()
