from os.path import abspath, dirname


PATH_ROOT           = dirname(dirname(abspath(__file__)))

PATH_DATASTORE      =  PATH_ROOT + '/datastore'

FILE_RETENTION_TIME = 10 # in minutes
