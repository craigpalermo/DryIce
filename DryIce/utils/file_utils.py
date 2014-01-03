from   datetime   import datetime, timedelta
from   time       import sleep
from   operator   import itemgetter
from   boto.s3.connection import S3Connection
from   redis      import Redis
from   DryIce.settings import ACCESS_KEY, SECRET_ACCESS_KEY, BUCKET, \
                                FILE_RETENTION_TIME, TZ_OFFSET, REDIS_ADDRESS
                                
r_server = Redis(REDIS_ADDRESS)

def setup_bucket():
    conn = S3Connection(ACCESS_KEY, SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(BUCKET)
    return bucket

def delete_redis_entry(filename):
    ez_link = r_server.get(filename)
    r_server.delete(ez_link, filename)

def get_file_info(session_id):
    '''
    Returns list of dictionaries in this form for all files in the bucket
    that have a session_id matching the function parameter:
    [{'name': FILENAME, 'created': TIME_CREATED},...]
    '''
    files = []
    keys = get_session_keys(session_id)
        
    for key in keys:
        temp_time = key.last_modified[:-5] # todo, replace w/ regex instead
        file_time = datetime.strptime(temp_time,"%a, %d %b %Y %H:%M:%S")
        file_time = file_time - timedelta(hours=TZ_OFFSET)
        files.append({'name': key.name.name, 'created': file_time})
    sorted_files = sorted(files, key=itemgetter('created'), reverse=True)
    return sorted_files

def get_session_keys(session_id):
    '''
    Get list of key objects for session matching id
    '''
    keys = []
    bucket= setup_bucket()
    prefix = "%s/" % (session_id,)
    for key in bucket.list(prefix=prefix):
        k = bucket.lookup(key)
        if k.get_metadata('session_id') == session_id:
            keys.append(k)
    return keys

def expire_files():
    '''
    Delete from bucket all files that are older than FILE_RETENTION_TIME.
    '''
    bucket = setup_bucket()
    
    while(True):
        print "Removing old files..."
        to_delete = []
        for key in bucket.list():
            tmp = key.last_modified[:-5] # replace w/ regex later
            tmp = datetime.strptime(tmp, "%Y-%m-%dT%H:%M:%S")
            age = datetime.now() - tmp
                   
            #print tmp
            #print datetime.now()

            if age > timedelta(minutes=FILE_RETENTION_TIME):
                # print "Deleting %s" % (key.name.encode('utf-8'))
                delete_redis_entry(key.name)
                to_delete.append(key)
        bucket.delete_keys(to_delete)
        sleep(60)

def delete_session_keys(session_id):
    '''
    Delete all files uploaded by session with parameter id
    '''
    bucket = setup_bucket()
    keys = get_session_keys(session_id)
    to_delete = []

    for key in keys:
        to_delete.append(key.name.name)
   
    delete_redis_entry(to_delete)
    bucket.delete_keys(to_delete)

def generate_ez_link():
    rw = RandomWords()
    return rw.random_word().capitalize() + rw.random_word().capitalize()
