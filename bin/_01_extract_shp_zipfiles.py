from F477_legacy_maker import CoverageMaker, unzipper
from F477_legacy_maker.CoverageMaker import pd
import my_paths
import os


def extract_zipfiles(run=False, copy_from_k=False, unzip=False):
    """

    :rtype: object
    :param run: IF true the function will will be live.
    :param copy_from_k: Copy zips from K drive
    :param unzip: Run unzip file

    """

    if run:
        print('fun')
        if copy_from_k is True:
            print('another fun')
            shp_df = pd.read_excel(my_paths.shp_excel_path, 'INVENTORY', engine='openpyxl')
            # print(shp_df[shp_df['legacy_support_recipient']==True]['file_path'])

            recippient = shp_df[(shp_df['legacy_support_recipient'] == True) & (shp_df['upload_type'] == 'MWBD')]

            for file_path, pid, pname in zip(recippient['file_path'], recippient['provider_id'], recippient['provider_name']):
                print(file_path)
                unzipper.Unzipper.copy_zip_file(file_path,
                            os.path.join(CoverageMaker.int_paths.zipfolder_path, "__{}_{}__{}".format(pid,
                                                                                                      pname,
                                                                                                      os.path.basename(file_path))))

        if unzip is True:

            print('unzipping')
            unzipper.Unzipper(base_input_folder=CoverageMaker.int_paths.zipfolder_path,
                              base_output_folder=CoverageMaker.int_paths.zipfolder_path).unzip(list=True, wildcard="*")
