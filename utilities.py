import os

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class hashing:
  @staticmethod
  def hashfile(file_path):
    hash = os.popen("sha1sum " + file_path + " | cut -d' ' -f1").read().replace('\n','')
    return hash

class savingToDb:
  @staticmethod
  # Method to save file to DB
  def saveFileToDB(conn, full_path, file_name):
    conn.execute("INSERT INTO FILES (FILE_PATH,FILE_HASH) \
        VALUES('" + full_path + file_name + "', '" + hashing.hashfile(full_path + file_name) + "');");
  @staticmethod
  # Method to get the dir files
  def getFilesList(full_path,conn):
    list_of_files = os.listdir(full_path)
    list_of_dirs = next(os.walk(full_path))[1]
    for file_name in list_of_files:
      if full_path[-1] != "/":
        full_path = full_path + "/"
      if os.path.isfile(full_path + file_name):
        savingToDb.saveFileToDB(conn, full_path, file_name)
    for dir_name in list_of_dirs:
      if os.path.isdir(dir_name):
        savingToDb.getFilesList(full_path + dir_name,conn)
