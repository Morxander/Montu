#!/usr/bin/python
import sqlite3
import os
from utilities import bcolors
from utilities import savingToDb

# Printing Logo
print bcolors.HEADER + """
-----------------------------------
|  ___  ___            _          |
|  |  \/  |           | |         |
|  | .  . | ___  _ __ | |_ _   _  |
|  | |\/| |/ _ \| '_ \| __| | | | |
|  | |  | | (_) | | | | |_| |_| | |
|  \_|  |_/\___/|_| |_|\__|\__,_| |
|                                 |
|         Version 0.1             |
|       By : Morad Edwar          |
-----------------------------------
"""
# some needed vars
full_path = ""
changed_files = []
new_files = []
# connection to the database
conn = sqlite3.connect("files.db")
print bcolors.OKGREEN + "Opened database successfully"
# Geting the path to check
path_cursor = conn.execute("SELECT * FROM SETTINGS where OPTION_KEY='full_path'")
full_path = path_cursor.fetchone()[1]
print bcolors.OKGREEN + "Fetched the path (" + full_path + ")"
# Check for the changes on the old files
old_files = conn.execute("SELECT * FROM FILES")
for file_path in old_files:
    hash = os.popen("sha1sum " + file_path[0] + " | cut -d' ' -f1").read().replace('\n','')
    if hash != file_path[1]:
        print bcolors.WARNING + file_path[0] + " File Changed"
        changed_files.append(file_path[0])
    else:
        print bcolors.ENDC + file_path[0] + " Still Unchanged"
# Check for new files
# Method to get all dirs and files for a path
def getFileAndDirs(full_path):
    list_of_files = os.listdir(full_path)
    list_of_dirs = next(os.walk(full_path))[1]
    for file_name in list_of_files:
        if full_path[-1] != "/":
            full_path = full_path + "/"
        if os.path.isfile(full_path + file_name):
            is_exist = conn.execute("SELECT * FROM FILES WHERE FILE_PATH='" + full_path + file_name + "'")
            if len(is_exist.fetchall()) == 0:
                new_files.append(full_path + file_name)
                print bcolors.FAIL + full_path + file_name + " New File"
    for dir_name in list_of_dirs:
        if os.path.isdir(dir_name):
            getFileAndDirs(full_path + dir_name)
# Run the method on the current path
getFileAndDirs(full_path)
