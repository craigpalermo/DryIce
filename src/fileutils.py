import os
import traceback

from   os         import listdir
from   os.path    import getmtime, isfile, join, splitext
from   datetime   import datetime, timedelta
from   time       import ctime, sleep
from   werkzeug   import secure_filename
from   constants  import *
from   operator   import itemgetter

def list_files():
    '''
    returns list containing names of all files in datastore
    '''
    return [f for f
        in listdir(PATH_DATASTORE)
        if isfile(join(PATH_DATASTORE, f))]

def get_file_info():
    '''
    Returns a list of dictionaries as such: 
    [{'name': FILENAME, 'created': TIME_CREATED},...]
    '''
    files = []
    try:
        for f in list_files():
            temp_time = ctime(getmtime(
                PATH_DATASTORE + '/' + f))
            file_time = datetime.strptime(temp_time,
                    "%a %b %d %H:%M:%S %Y")
            files.append({'name': f, 'created': file_time})
    except: pass
    sorted_files = sorted(files, key=itemgetter('created'), reverse=True)
    return sorted_files


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
