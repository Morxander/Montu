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
# Opening the database file for writing
conn = sqlite3.connect("files.db")
print bcolors.OKGREEN + "Opened database successfully"
# Creating the settings table
conn.execute('''CREATE TABLE SETTINGS
       (OPTION_KEY           TEXT    NOT NULL,
        OPTION_VALUE         TEXT     NOT NULL);''')
print bcolors.OKGREEN + "Created settings table successfully"
# Creating the files table
conn.execute('''CREATE TABLE FILES
       (FILE_PATH           TEXT    NOT NULL,
       FILE_HASH           TEXT     NOT NULL,
       UPDATED_AT          TEXT);''')
print bcolors.OKGREEN + "Created files table successfully"
# Let's start the magic
email = raw_input(bcolors.ENDC + "Please enter your email to send the report : ")
full_path = raw_input(bcolors.ENDC + "Please enter the full path to monitor : ")
while not os.path.exists(full_path) or not os.path.isdir(full_path):
    full_path = raw_input(bcolors.FAIL + "Please enter valid full path to monitor : ")
# Saving the path to the settings table
conn.execute("INSERT INTO settings (OPTION_KEY,OPTION_VALUE) VALUES('full_path', '"+full_path+"');");
conn.execute("INSERT INTO settings (OPTION_KEY,OPTION_VALUE) VALUES('email', '"+email+"');");
conn.commit()
print bcolors.OKGREEN + "Path saved successfully"
# Saving the files list
savingToDb.getFilesList(full_path, conn)

conn.commit()
conn.close()
