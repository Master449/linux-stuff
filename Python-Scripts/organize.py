"""
Titel: Downloads organizer
Author: Jan B.
Date: april 2020
Version: 1.0
Python-version: 3.7

This program is designed to organize the contents of a folder by assigning
files with specific extensions to specific folders.
This program is made with the purpose of organzing the windows download-folder,
but by changing the directory_path-variable in the main it can tho(probably) be
used for any folder.
The directories-dictionary in the main specifies the names of the folders as
well as the file extensions that should be assigned to those folders.
You can change this dictionary to suit your needs.


MIT License

Copyright (c) [2020] [Jan B.]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# imports:
import os
import shutil
import sys


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
    if "OTHER" not in os.listdir(directory_path):
        os.mkdir(os.path.join(directory_path, "OTHER"))


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
                if file.endswith(extension):
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
    directory_path = "/home/david/Downloads"
    directories = {
        "WebDev": (".html5", ".html", ".htm", ".xhtml", ".js", ".css", ".scss", ".vue"),
        "Images": (".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg", ".heif", ".psd"),
        "Videos": (".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng", ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"),
        "Documents": (".pdf", ".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods", ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox", ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt", "pptx"),
        "Compressed": (".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z", ".dmg", ".rar", ".xar", ".zip", ".bz2", "tar.gz", ".tar.xz", ".tar.zst", ".img", ".img.bs2"),
        "Audio": (".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3", ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"),
        "Plaintext": (".txt", ".in", ".out"),
        "Java": ".jar",
        "Python": ".py",
        "Executable": (".exe", ".pkg", ".deb", ".AppImage"),
        "Others": ""
    }
    try:
        create_folders(directories, directory_path)
        organize_folders(directories, directory_path)
        organize_remaining_files(directory_path)
        #organize_remaining_folders(directories, directory_path)
    except shutil.Error:
        print("There was an error trying to move an item to its destination folder")

