import os
import shutil
from filecmp import cmp

from utils import *


def synchronize_folders(source_path, destination_path, logger_path):
    log("Synchronization operation started.", logger_path)
    source_files, source_directories = read_files_and_directories_in_folder(source_path)
    destination_files, destination_directories = read_files_and_directories_in_folder(destination_path) 

    # We will start with syncronizing the internal directories in the two folders first.
    source_directory_set = set(source_directories)
    destination_directory_set = set(destination_directories)
    directories_to_delete = destination_directory_set - source_directory_set
    directories_to_create = source_directory_set - destination_directory_set

    # We will delete directories in destination folder which are absent in source folder.
    for directory in directories_to_delete:
        directory_to_delete = os.path.join(destination_path, directory)
        try:
            shutil.rmtree(directory_to_delete, onerror=handle_access_errors)
            log(f"Directory \"{directory_to_delete}\" deleted in destination folder.", logger_path)
        except Exception as e:
            log(f"Failed to delete directory \"{directory_to_delete}\" in destination folder: {e}", logger_path, is_error=True)

    # We will create directories in destination folder which are present in source folder.
    for directory in directories_to_create:
        directory_to_create = os.path.join(destination_path, directory)
        try:
            os.makedirs(directory_to_create)
            log(f"New Directory \"{directory_to_create}\" created in destination folder.", logger_path)
        except Exception as e:
            log(f"Failed to create directory \"{directory_to_create}\" in destination folder: {e}", logger_path, is_error=True)

    # Now we will move on and synchronize files in both folders.
    source_file_set = set(source_files)
    destination_file_set = set(destination_files)
    files_to_delete = destination_file_set - source_file_set
    files_to_create = source_file_set - destination_file_set
    files_to_compare = source_file_set & destination_file_set

    # Identify if a file common in two folders varies in content or not.
    for file in files_to_compare:
        source_file = os.path.join(source_path, file)
        destination_file = os.path.join(destination_path, file)
        if not cmp(source_file, destination_file, shallow=False):
            files_to_create.add(file)
            files_to_delete.add(file)

    # Modifying common files in both folders to match content.
    files_to_modify = files_to_create & files_to_delete
    for file in files_to_modify:
        source_file = os.path.join(source_path, file)
        destination_file = os.path.join(destination_path, file)
        try:
            shutil.copy(source_file, destination_file)
            log(f"File \"{destination_file}\" modified in destination folder.", logger_path)
        except Exception as e:
            log(f"Failed to modify \"{destination_file}\" in destination folder: {e}", logger_path, is_error=True)

    # Creating files in destination folder which are present in source folder.
    for file in files_to_create - files_to_modify:
        source_file = os.path.join(source_path, file)
        destination_file = os.path.join(destination_path, file)
        try:
            shutil.copy(source_file, destination_file)
            log(f"New File \"{destination_file}\" created in destination folder.", logger_path)
        except Exception as e:
            log(f"Failed to create \"{destination_file}\" in destination folder: {e}", logger_path, is_error=True)

    # Deleting files in destination folder which are absent in source folder.
    for file in files_to_delete - files_to_modify:
        source_file = os.path.join(source_path, file)
        destination_file = os.path.join(destination_path, file)
        try:
            if os.path.isfile(destination_file):
                os.remove(destination_file)
                log(f"File \"{destination_file}\" deleted in destination folder.", logger_path)
        except Exception as e:
            log(f"Failed to delete \"{destination_file}\" in destination folder: {e}", logger_path, is_error=True)

    log("Synchronization operation completed.", logger_path)