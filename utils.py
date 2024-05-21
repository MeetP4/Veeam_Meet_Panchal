import datetime
import os
import stat


# Function to log messages in the desired log file.
def log(message, logger_path, is_error=False):
    timestamp = datetime.datetime.now()
    print(f"{message}")
    if not is_error:
        log_message = f"INFO: {timestamp}: {message}"
    else:
        log_message = f"ERROR: {timestamp}: {message}"
    
    with open(logger_path, "a") as log:
        log.write(log_message + '\n')


# Function to scan source and destination folders for files and directories.
def read_files_and_directories_in_folder(path):
    file_names, dir_names = [], []
    for root, directories, files in os.walk(path):
        for file in files:
            file_names.append(os.path.relpath(os.path.join(root, file), path))
        for directory in directories:
            dir_names.append(os.path.relpath(os.path.join(root, directory), path))

    return file_names, dir_names


# To handle permission errors, especially in windows, while trying to remove sub-folders.
def handle_access_errors(func, path, exc_info):
    exc_type, _ , _ = exc_info
    if exc_type is PermissionError:
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise