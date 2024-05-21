import argparse
import os
import sys
import time

from synchronize_folders import synchronize_folders
from utils import log


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--destination', required=True)
    parser.add_argument('--log', required=True)
    parser.add_argument('--time', help='Time period of synchronization in seconds', required=True)
    arguments = parser.parse_args()
    
    source_path = arguments.source
    destination_path = arguments.destination
    logger_path = arguments.log
    time_period = int(arguments.time)

    if not os.path.exists(source_path):
        log("Source folder does not exist.",logger_path)
        sys.exit(1)

    if not os.path.exists(destination_path):
        log("Destination folder does not exist.",logger_path)
        sys.exit(1)

    try:
        while True:
            synchronize_folders(source_path, destination_path, logger_path)
            time.sleep(time_period)
    except KeyboardInterrupt:
        log("Aborting Synchronization Procedure.", logger_path)
        sys.exit(0)


if __name__ == "__main__":
    main()