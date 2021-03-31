import zipfile36 as zipfile
import os
import fnmatch
from shutil import copyfile
from F477_legacy_maker import logger

class Unzipper:


    """
    This object class will unzip fiels

    """



    def __init__(self, base_input_folder=None, base_output_folder=None):
        self.base_input_folder = base_input_folder
        self.base_output_folder = base_output_folder
        self.parsed_path_list = []
        self.zip_path = []


    def path_grabber(self, wildcard=None):

        for root, dirs, files in os.walk(self.base_input_folder):
            for file in fnmatch.filter(files, wildcard):
                self.parsed_path_list.append(os.path.join(root, file))
        print("i found {} file(s)".format(len(self.parsed_path_list)))


    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def unzip(self, list=True, wildcard=None):
        print('unzipping')
        """
        :param list: if True, path_grabber class method will look for base path based on wildcard
        from self.parsed_path and return a list of zip paths.
        """

        if list:

            Unzipper.path_grabber(self, wildcard=wildcard)

        for file_path in self.parsed_path_list:
            output = os.path.join(self.base_output_folder,os.path.basename(file_path).strip('.zip'))
            try:
                with zipfile.ZipFile(file=file_path, mode='r') as zip_ref:
                    if not os.path.exists(os.path.join(self.base_output_folder,os.path.basename(file_path).strip(".zip"))):
                        #print("dir does not exits")
                        os.makedirs(output)
                        zip_ref.extractall(path=output)
                    else:
                        print("zip exists")
            except zipfile.BadZipFile:
                print("Error: Zip file is corrupted")

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def copy_zip_file(self, src, dist):
        copyfile(src, dist)
        print("file copied to : {}".format(dist))

        