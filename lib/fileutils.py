import os
import traceback

from   os         import listdir
from   os.path    import getmtime, isfile, join, splitext
from   datetime   import datetime, timedelta
from   time       import ctime, sleep

from .constants   import *


def list_files():
    return [f for f
        in listdir(PATH_DATASTORE)
        if isfile(join(PATH_DATASTORE, f))]


def upload_file(data):
    name, ext = splitext(data.filename)
    raw       = data.file.read() # small files =.=
    filename  = data.filename
    with open(PATH_DATASTORE + '/' + filename, 'w') as f:
        f.write(raw)


def get_file_info():
    files = []
    try:
        for f in list_files():
            temp_time = ctime(getmtime(
                PATH_DATASTORE + '/' + f))
            file_time = datetime.strptime(temp_time,
                    "%a %b %d %H:%M:%S %Y")
            files.append({'name': f, 'created': file_time})
    except: pass
    return files


def expire_files():
    '''
    Delete from disk all files that are older than FILE_RETENTION_TIME.
    '''
    while(True):
        for f in list_files():
            try:
                tmp = ctime(getmtime(PATH_DATASTORE + '/' + f))
                age = datetime.now() - datetime.strptime(tmp,
                        "%a %b %d %H:%M:%S %Y")
                if age > timedelta(minutes=FILE_RETENTION_TIME):
                    os.remove(PATH_DATASTORE + '/' + f)
            except:
                print("error statting files - " + traceback.format_exc())
        sleep(60)
