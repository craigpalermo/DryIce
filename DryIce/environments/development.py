import os
import django

# calculated paths for django and the site
# used as starting points for various other paths
ENV_ROOT = os.path.dirname(os.path.realpath(__file__))

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database info
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': ENV_ROOT + '/sqlite.db',                      # Or path to database file if using sqlite3.
#         'USER': '',                      # Not used with sqlite3.
#         'PASSWORD': '',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dryice',                      # Or path to database file if using sqlite3.
        'USER': 'cpalermo',                      # Not used with sqlite3.
        'PASSWORD': 'RHAsmidan1346c',                  # Not used with sqlite3.
        'HOST': 'dryice-dev.cgull5itjlsk.us-west-2.rds.amazonaws.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Time zone offset for file creation times, set to 0 for production
TZ_OFFSET = 5

# File storage parameters
FILE_RETENTION_TIME = 30 
MB_UPLOAD_LIMIT = 512
MAX_CONTENT_LENGTH = 512 * 1024 * 1024

# S3 Credentials
BUCKET = "dryice-dev"
ACCESS_KEY = "AKIAJY4PLTKEW3V6DPFQ"
SECRET_ACCESS_KEY = "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"

# Redis
REDIS_ADDRESS = "localhost"
