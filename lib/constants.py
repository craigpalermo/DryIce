from os.path import abspath, dirname


PATH_ROOT           = dirname(dirname(abspath(__file__)))

PATH_DATASTORE      =  PATH_ROOT + '/datastore'

FILE_RETENTION_TIME = 10 # in minutes

MAX_CONTENT_LENGTH = 512 * 1024 * 1024 # Max upload size is 1024 MB
