import os
import traceback

from   os         import listdir
from   os.path    import getmtime, isfile, join, splitext
from   datetime   import datetime, timedelta
from   time       import ctime, sleep
from   werkzeug   import secure_filename
from   constants  import *
from   operator   import itemgetter
from   boto.s3.connection import S3Connection


def setup_bucket():
    conn = S3Connection(ACCESS_KEY, SECRET_ACCESS_KEY)
    bucket = conn.get_bucket('storage.dropbucket')
    return bucket

def get_file_info():
    '''
    Returns a list of dictionaries as such: 
    [{'name': FILENAME, 'created': TIME_CREATED},...]
    '''
    files = []
    bucket = setup_bucket()
    try:
        for key in bucket.list():
            temp_time = key.last_modified[:-5] # todo, replace w/ regex instead
            file_time = datetime.strptime(temp_time,"%Y-%m-%dT%H:%M:%S")
            file_time = file_time - timedelta(hours=5) # hardcoded for EST
            files.append({'name': key.name.encode('utf-8'), 'created': file_time})
    except: pass
    sorted_files = sorted(files, key=itemgetter('created'), reverse=True)
    return sorted_files


def expire_files():
    '''
    Delete from bucket all files that are older than FILE_RETENTION_TIME.
    '''
    bucket = setup_bucket()
    
    while(True):
        print "Removing old files..."
        to_delete = []
        for key in bucket.list():
            try:
                tmp = key.last_modified[:-5] # replace w/ regex later
                tmp = datetime.strptime(tmp, "%Y-%m-%dT%H:%M:%S")
                #tmp = tmp - timedelta(hours=8) # adjust for PST
                tmp = tmp - timedelta(hours=5) # adjust for EST
                age = datetime.now() - tmp
                       
                #print tmp
                #print datetime.now()
 
                if age > timedelta(minutes=FILE_RETENTION_TIME):
                    # print "Deleting %s" % (key.name.encode('utf-8'))
                    to_delete.append(key)
            except:
                print("error statting files - " + traceback.format_exc())
        bucket.delete_keys(to_delete)
        sleep(60)

