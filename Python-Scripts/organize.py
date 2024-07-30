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

    directory_path = str(Path.home() / "Downloads")
    
    

    directories = {
        "Development": (".html5", ".html", ".htm", ".xhtml", ".js", ".css", ".scss", ".vue", ".jar", ".class", ".cpp", ".cc", ".c", ".py", ".log", ".json"),
        "Images": (".jpeg", ".JPEG", ".jpg", ".JPG", ".tiff", ".gif", ".bmp", ".png", ".PNG", ".bpg", "svg", ".heif", ".psd", ".webp"),
        "Videos": (".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng", ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"),
        "Documents": (".pdf", ".PDF", ".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods", ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox", ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt", "pptx", ".csv"),
        "Compressed": (".a", ".ar", ".cpio", ".tar", ".gz", ".rz", ".7z", ".dmg", ".rar", ".xar", ".zip", ".bz2", "tar.gz", ".tar.xz", ".tar.zst", ".img.bs2"),
        "BootMedia": (".iso", ".img"),
        "Audio": (".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3", ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"),
        "Plaintext": (".txt", ".in", ".out"),
        "Executable": (".exe", ".pkg", ".deb", ".AppImage"),
        "3D Models": (".obj", ".stl"),
        "Torrents": ".torrent"
    }

    development_directories = {
        "Python": ".py",
        "Java": (".jar", ".class"),
        "WebDev": (".html5", ".html", ".htm", ".xhtml", ".js", ".css", ".scss", ".vue"),
        "C": (".cpp", ".cc", ".h", ".c")
    }

    try:
        create_folders(directories, directory_path)
        create_folders(development_directories, str(os.path.join(directory_path, "Development")))

        
        organize_folders(directories, directory_path)
        organize_folders(development_directories, str(os.path.join(directory_path, "Development")))

    except shutil.Error:
        print("There was an error trying to move an item to its destination folder")

