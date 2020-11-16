import os
from drive import *

from links import *


path = os.getcwd()
path_files = os.path.join(path, "files")
path_tmp = os.path.join(path, "tmp")



pull_file(path, VERSION_LINKS, "versions.csv")

versions = convert_version_to_dictionary(path_files)
online_version = convert_version_to_dictionary(path_tmp)

architecture = list(online_version.keys())[1:]

if verify_architecture(path, architecture):
    print("Architecture OK")

for topic in online_version:
    if not verify_version(versions, online_version, topic):
        print(f"{topic} not up to date")

delete_tmp(path)
