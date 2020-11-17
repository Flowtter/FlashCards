import os
from google_drive_downloader import GoogleDriveDownloader as gdd
import utils


def pull_file(path_tmp, link, name):
    """Pull a GDRIVE file

    Args:
        path (string): path to save
        link (string): link to download
        name (string): name to save
    """
    path_tmp_main_version = os.path.join(path_tmp, name)

    if not utils.verify_folder(path_tmp):
        utils.mkdir(path_tmp)
    
    gdd.download_file_from_google_drive(file_id=link, dest_path=path_tmp_main_version)
    with open(path_tmp_main_version, "r") as f:
        if f.readline()[0] == "<":
            # TO-DO ERROR HANDLING
            print(f"ERROR DOWNLOADING {link} AT {path_tmp_main_version} TIME OUT")
            exit()


def update_version(topic, path, links):
    path_local_topic = os.path.join(path, "files", topic)
    path_tmp = os.path.join(path, "tmp")

    path_tmp_topic = os.path.join(path_tmp, topic)
    path_tmp_topic_link = os.path.join(path_tmp_topic, "versions.csv")

    utils.mkdir(path_tmp_topic)
    link = links[topic]

    pull_file(path_tmp_topic, link, "versions.csv")

    version = utils.convert_file_to_dictionary(path_local_topic, "versions.csv")
    online_version = utils.convert_file_to_dictionary(path_tmp_topic, "versions.csv")

    architecture_online = list(online_version.keys())
    download_link = online_version["link"]

    architecture_online = list(online_version.keys())[1:]  # First ellement is link

    not_downloaded = True

    for sub_topic in architecture_online:
        state = utils.verify_version(version, online_version, sub_topic)
        if state:
            if not_downloaded:  # Get list of all links
                not_downloaded = False
                pull_file(path_tmp_topic, download_link, "topics_links.csv")
                link_dictionary = utils.convert_file_to_dictionary(path_tmp_topic, "topics_links.csv")
            print(f"{sub_topic} in {topic} not up to date")
            pull_file(path_tmp_topic, link_dictionary[sub_topic], str(sub_topic)+".csv")

        

    
