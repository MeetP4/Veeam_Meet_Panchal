# ONE WAY SYNCHRONIZATION
Solution for Veeam QA Test in Python. <br />
Author: Meet Rajkumar Panchal

# How to Run?
Prerequisite: Python 3
```console
python main.py --source SOURCE_PATH  --destination DESTINATION_PATH --log LOG_PATH --time SYNC_PERIOD
```
or 
```console
py main.py --source SOURCE_PATH  --destination DESTINATION_PATH --log LOG_PATH --time SYNC_PERIOD
```
* SOURCE_PATH: path of the source folder in your system.
* DESTINATION_PATH: path of the destination folder that you want to be replicated in your system.
* LOG_PATH: path of the log file in your system.
* SYNC_PERIOD: time period in seconds, after which the program would run the synchronization procedure again.

In order to abort the process, Keyboard Interrupt is required.

# Python Libraries Required:
* os
* sys
* time
* argparse
* shutil
* filecmp
* stat
* datetime
