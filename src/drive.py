import os
from google_drive_downloader import GoogleDriveDownloader as gdd
from utils import *


def pull_file(path, link, name):
    """Pull a GDRIVE file

    Args:
        path (string): path to save
        link (string): link to download
        name (string): name to save
    """
    path_tmp = os.path.join(path, "tmp")
    path_tmp_main_version = os.path.join(path_tmp, name)

    if not mkdir(path_tmp):
        mkdir(path_tmp)
    
    try:
        gdd.download_file_from_google_drive(file_id=link, dest_path=path_tmp_main_version)
    except:
        # TO-DO ERROR HANDLING
        print(f"ERROR DOWNLOADING {link} AT {path_tmp_main_version}")
        exit()
    