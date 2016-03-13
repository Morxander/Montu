# Montu

Montu is a tool to monitor your website files, Basically it saves the sha1sum of the files in a SQLite Database and you set a cronjob to start the checker whenever you want.
Montu was a falcon-god of war in Ancient Egyptian religion, And Montu will fight the war for you against any attackers.

### Requirements
Just make sure you have installed : 
* sqlite3
* python-sqlite
 
 
    sudo apt-get install sqlite3 python-sqlite

Then clone this repo on a user which have access to your website files :

    git clone git@github.com:Morxander/Montu.git

Navigate to the project dir :
    
    cd Montu
Make sure that `install.py` has execution permission :
    
    chmod 755 install.py
Then just run it and follow the instructions :

    ./install.py

### ToDo:

* Asking for an email during the installation
* Checking for files changes
* Checking for the new files
* Allow to manually update the files hashes in the Database
* Sending an Email Report

### Version
0.1

### License
GPL 2

**Free Software, Hell Yeah!**
