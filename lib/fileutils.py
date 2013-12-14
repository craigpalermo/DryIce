import os
import traceback

from   os         import path
from   datetime   import datetime, timedelta

from   .          import *
from   .fileutils import list_files


def upload_file(data):
    name, ext = path.splitext(data.filename)
    # data.save(datastore_path)

    raw = data.file.read() # small files =.=
    filename = data.filename
    with open(PATH_DATASTORE + '/' + filename, 'w') as f:
        f.write(raw)


def get_file_info():
    files = []
    try:
        for f in list_files():
            temp_time = time.ctime(path.getmtime(
                datastore_path + '/' + f))
            file_time = datetime.strptime(temp_time,
                    "%a %b %d %H:%M:%S %Y")
            files.append({'name': f, 'created': file_time})
    except: pass
    return files

def expire_files():
    '''
    Removes from the datastore directory all files that have modified
    time older than FILE_RETENTION_TIME
    '''
    while(True):
        files = list_files()
        for f in files:
            try:
                temp = time.ctime(path.getmtime(datastore_path + '/' + f))
                age = datetime.now() - datetime.strptime(temp, "%a %b %d %H:%M:%S %Y")
                if age > timedelta(minutes=FILE_RETENTION_TIME):
                    os.remove(datastore_path + '/' + f)
            except:
                print("error statting files - " + traceback.format_exc())
        time.sleep(60)
