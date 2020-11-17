import os
import csv
import shutil

import distutils
from distutils import dir_util
import error

def mkdir(path):
    """Create a Directory

    Args:
        path (string): path to create

    Returns:
        [bool]: sucess
    """
    try:
        os.mkdir(path)
        return True
    except OSError:
        return False


def verify_folder(path):
    """Verify that the folder exists

    Args:
        path (string): path to create

    Returns:
        bool: exists
    """
    return os.path.exists(path)


def create_architecture(path, expected):
    """Create the files architecture

    Args:
        path (path): path to create
        expected (list[string]): folders array

    Returns:
        bool: sucess
    """
    for folder in expected:
        if not verify_folder(folder):
            mkdir(os.path.join(path, folder))
    return True


def verify_and_update_architecture(path, expected):
    """Verify the architecture and update it

    Args:
        path (path): path to verify
        expected (list[string]): folders array

    Returns:
        bool: sucess
    """
    path_notes = os.path.join(path, "files")
    if not verify_folder(path_notes):
        mkdir(path_notes)
        return create_architecture(path_notes, expected)
    for root, dirs, files in os.walk(path_notes):
        if root == path_notes:
            if len(dirs) != len(expected):
                return create_architecture(path_notes, expected)
            else:
                if len(set(dirs).intersection(expected)) != len(dirs):
                    return create_architecture(path_notes, expected)
        return True


def convert_file_to_dictionary(path, name):
    """Convert file.csv to dictionary

    Args:
        path (string): path to load
        path (name): name to save

    Returns:
        dict: dictionary
    """
    path_file = os.path.join(path, name)
    if not os.path.exists(path_file):
        with open(path_file, "w") as f_version:
            f_version.write("main,0")
            return {"main":0}
    dictionary = {}
    with open(path_file, "r") as f_version:
        reader = csv.reader(f_version, delimiter=',')
        for row in reader:
            dictionary[row[0]] = row[1]
    return dictionary


def verify_version(local :dict, online :dict, topic):
    """Verify that local version is up to date

    Args:
        local (dict): local dictionary
        online (dict): online dictionary
        topic (string): topic in dictionary

    Returns:
        bool: the local version is outdated
    """
    if topic in local:
        if int(online[topic]) < int(local[topic]):
            delete_folder(os.path.join(os.getcwd(), "tmp"))
            raise error.VersionAhead("VERSION LOCAL AHEAD, ABORTING")
        return int(online[topic]) > int(local[topic])
    return True


def delete_folder(path):
    """Delete folder folder

    Args:
        path (string): path to delete

    Returns:
        bool: sucess
    """
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        return True
    return False


def handle_tmp(path_files, path_tmp):
    """Copy tmp files and remove tmp folder

    Args:
        path_files (string): path to files
        path_tmp (string): path to tmp
    """
    distutils.dir_util.copy_tree(path_tmp, path_files)
    delete_folder(path_tmp)


def dictionary_to_csv(path, name, dictionary :dict):
    """Save a dictionary to csv

    Args:
        path (string): path to save
        name (string): name to save
        dictionary (dict): dictionary to save
    """
    path_csv = os.path.join(path, name)
    with open(path_csv, "w") as f_csv:
        for key in dictionary.keys():
            f_csv.write("%s,%s\n"%(key,dictionary[key]))
        

def update_version(path_files):
    """Update version with update.csv file

    Args:
        path_files (string): path to load file
    """
    path_update = os.path.join(path_files, "update.csv")

    if not os.path.exists(path_update):
        with open(path_update, "w"):
            pass
        return

    path_version = os.path.join(path_files, "versions.csv")
    topics, sub_topics = [], []
    with open(path_update, "r") as f_update:
        reader = csv.reader(f_update, delimiter=',')
        for row in reader:
            topics.append(row[0])
            sub_topics.append(row[1:])
    if topics:
        version = convert_file_to_dictionary(path_files, "versions.csv")
        index = 0
        for topic in topics:
            version[topic] = str(int(version[topic])+1)
            path_sub_topic = os.path.join(path_files, topic)
            sub_version = convert_file_to_dictionary(path_sub_topic, "versions.csv")
            for sub_topic in sub_topics[index]:
                if sub_topic != "link":
                    sub_version[sub_topic] = str(int(sub_version[sub_topic])+1)
            dictionary_to_csv(path_sub_topic, "versions.csv", sub_version)
            index += 1

        version["main"] = str(int(version["main"])+1)

        dictionary_to_csv(path_files, "versions.csv", version)
    os.remove(path_update)
    with open(path_update, "w"):
        pass
