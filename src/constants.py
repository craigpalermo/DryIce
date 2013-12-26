from os.path import abspath, dirname

PATH_ROOT           = dirname(dirname(abspath(__file__)))

PATH_DATASTORE      =  PATH_ROOT + '/datastore'

# Number of minutes files remain in storage
FILE_RETENTION_TIME = 30 

# S3 Credentials
BUCKET = "dropbucket-datastore"
ACCESS_KEY = "AKIAJY4PLTKEW3V6DPFQ"
SECRET_ACCESS_KEY = "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"
