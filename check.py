#!/usr/bin/python
import sqlite3
import os
import sys
from utilities import bcolors

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
report_path = '/tmp/montu.log'
report = open(report_path, 'w')
# connection to the database
conn = sqlite3.connect("files.db")
# Get the email data
email_to = conn.execute("SELECT * FROM SETTINGS where OPTION_KEY='email'").fetchone()[1]
email_subject = conn.execute("SELECT * FROM SETTINGS where OPTION_KEY='email_subject'").fetchone()[1]
# Check for --update argument
args = str(sys.argv)
update = False
if '--update' in args:
    update = True
print bcolors.OKGREEN + "Opened database successfully"
# Geting the path to check
full_path = conn.execute("SELECT * FROM SETTINGS where OPTION_KEY='full_path'").fetchone()[1]
print bcolors.OKGREEN + "Fetched the path (" + full_path + ")"
# Check for the changes on the old files
old_files = conn.execute("SELECT * FROM FILES")
for file_path in old_files:
    hash = os.popen("sha1sum " + file_path[0] + " | cut -d' ' -f1").read().replace('\n', '')
    if hash != file_path[1]:
        print bcolors.WARNING + file_path[0] + " File Changed"
        report.write(file_path[0] + " File Changed\n")
        changed_files.append(file_path[0])
        if update:
            conn.execute("UPDATE FILES SET FILE_HASH='" + hash + "' WHERE FILE_PATH='" + file_path[0] + "'")
            conn.commit()
            print bcolors.WARNING + file_path[0] + " File Hash Updated"
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
                report.write(full_path + file_name + " New File\n")
                if update:
                    hash = os.popen("sha1sum " + full_path + file_name + " | cut -d' ' -f1").read().replace('\n','')
                    conn.execute("INSERT INTO FILES (FILE_PATH,FILE_HASH) values('" + full_path + file_name + "','"+hash+"');")
                    conn.commit()
                    print bcolors.WARNING + full_path + file_name + " New File Inserted"
    for dir_name in list_of_dirs:
        if os.path.isdir(dir_name):
            getFileAndDirs(full_path + dir_name)
# Run the method on the current path
getFileAndDirs(full_path)
# Close the log file
report.close()
# Send the report is there are new or changed files
if len(new_files) > 0 or len(changed_files) > 0:
    os.popen("mail -s '" + email_subject + "' " + email_to + " < " + report_path)
