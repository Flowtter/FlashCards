import os
import csv
import shutil
import distutils


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


def verify_architecture(path, expected):
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
        return online[topic] > local[topic]
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


def handle_tmp(path, path_tmp):
    path_files = os.path.join(path, "files")
    delete_folder(files)