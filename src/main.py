import os
import drive
import utils
import argparse

from links import LINKS_TOPICS, LINKS_VERSIONS

parser = argparse.ArgumentParser()
parser.add_argument("command")
args = parser.parse_args()

path = os.getcwd()
path_files = os.path.join(path, "files")
path_tmp = os.path.join(path, "tmp")

if __name__ == "__main__":
    if args.command == "pull":
        utils.mkdir(path_files)
        drive.pull_file(path_tmp, LINKS_VERSIONS, "versions.csv")

        versions = utils.convert_file_to_dictionary(path_files, "versions.csv")
        online_version = utils.convert_file_to_dictionary(path_tmp, "versions.csv")

        architecture = list(online_version.keys())[1:]

        if utils.verify_and_update_architecture(path, architecture):
            print("Architecture OK")

        for topic in online_version:
            if topic == "main":
                if utils.verify_version(versions, online_version, "main"):
                    print("Main not up to date. Donwloading links_topics")
                    drive.pull_file(path_tmp, LINKS_TOPICS, "links_topics.csv")
                    main_links_version = utils.convert_file_to_dictionary(path_tmp, "links_topics.csv")
                else:
                    print("Main is up to date")
                    break
            elif utils.verify_version(versions, online_version, topic):
                print(f"{topic} not up to date")
                drive.update_version(topic, path, main_links_version)

        utils.handle_tmp(path_files, path_tmp)
    if args.command == "update":
        utils.update_version(path_files)
