#!/usr/bin/python3
import os
import shutil
import sys
from pathlib import Path

def create_folders(directories, directory_path):
    """
    This function creates the folders in <directory_path> where the files
    will be moved to.
    :param directories: dictionary, this is a dictionary containing the
    names of the sorted folders and the extensions that correspond to those
    folders.
    :param directory_path: string, this is a string of the path to the
    directory that is to be sorted.
    """
    for key in directories:
        if key not in os.listdir(directory_path):
            os.mkdir(os.path.join(directory_path, key))


def organize_folders(directories, directory_path):
    """
    This function organizes the files in the specified folder into folders
    :param directories: directories: dictionary, this is a dictionary
    containing the names of the sorted folders and the extensions that
    correspond to those folders.
    :param directory_path: string, this is a string of the path to the
    directory that is to be sorted.
    """
    for file in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file)):
            src_path = os.path.join(directory_path, file)
            for key in directories:
                extension = directories[key]
                if file.endswith(tuple(extension)):
                    dest_path = os.path.join(directory_path, key, file)
                    shutil.move(src_path, dest_path)
                    break


def organize_remaining_files(directory_path):
    """
    This function assigns the file that don't have a corresponding folder to
    the <OTHER> directory.
    :param directory_path: string, this is a string of the path to the
    directory that is to be sorted.
    """
    for file in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file)):
            src_path = os.path.join(directory_path, file)
            dest_path = os.path.join(directory_path, "OTHER", file)
            shutil.move(src_path, dest_path)


def organize_remaining_folders(directories, directory_path):
    """
    This function assings the folders within the specified directory to the
    <FOLDER> directory.
    :param directories: directories: dictionary, this is a dictionary
    containing the names of the sorted folders and the extensions that
    corresponds to those folders.
    :param directory_path: string, this is a string of the path to the
    directory that is to be sorted.
    """
    list_dir = os.listdir(directory_path)
    organized_folders = []
    for folder in directories:
        organized_folders.append(folder)
    organized_folders = tuple(organized_folders)
    for folder in list_dir:
        if folder not in organized_folders:
            src_path = os.path.join(directory_path, folder)
            dest_path = os.path.join(directory_path, "FOLDERS", folder)
            try:
                shutil.move(src_path, dest_path)
            except shutil.Error:
                shutil.move(src_path, dest_path + " - copy")
                print("That folder already exists in the destination folder."
                      "\nThe folder is renamed to '{}'".format(folder + " - copy"))


if __name__ == '__main__':

    directory_path = str(Path.home() / "Downloads")

    directories = {
        "development": [".html5", ".html", ".htm", ".xhtml", ".js", ".css", ".scss", ".vue", ".jar", ".class", ".cpp", ".cc", ".c", ".py", ".log", ".json", ".xml", ".ttf", ".woff", ".woff2"],
        "images": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg", ".heif", ".psd", ".webp"],
        "videos": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng", ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
        "documents": [".pdf", ".PDF", ".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods", ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox", ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt", "pptx", ".csv"],
        "compressed": [".a", ".ar", ".cpio", ".tar", ".gz", ".rz", ".7z", ".dmg", ".rar", ".xar", ".zip", ".bz2", "tar.gz", ".tar.xz", ".tar.zst", ".img.bs2"],
        "boot-media": [".iso", ".img"],
        "audio": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3", ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
        "plaintext": [".txt", ".in", ".out"],
        "executable": [".exe", ".pkg", ".deb", ".AppImage"],
        "3d-models": [".obj", ".stl"],
        "torrents": [".torrent"]
    }

    development_subdir= {
        "python": [".py"],
        "java": [".jar", ".class"],
        "webdev": [".html5", ".html", ".htm", ".xhtml", ".js", ".css", ".scss", ".vue", ".ttf", ".woff", ".woff2"],
        "c": [".cpp", ".cc", ".h", ".c"],
        "xml": [".xml"]
    }

    for item in directories:
        directories[item] = directories[item] + [x.upper() for x in directories[item]]
    for item in development_subdir:
        development_subdir[item] = development_subdir[item] + [x.upper() for x in development_subdir[item]]

    try:
        create_folders(directories, directory_path)
        create_folders(development_subdir, str(os.path.join(directory_path, "development")))

        organize_folders(directories, directory_path)
        organize_folders(development_subdir, str(os.path.join(directory_path, "development")))

    except shutil.Error:
        print("There was an error trying to move an item to its destination folder")

