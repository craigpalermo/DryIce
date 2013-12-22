# Dropbucket
Simple way to _temporarily_ share files over the internet. No usernames or passwords, just a bucket with files in it.


## Install and run

    $ git clone git@github.com:unscsprt/dropbucket && cd ./dropbucket
    $ pip install -r requirements.txt
    $ python server.py


## Interface
- User goes to page, sees a list of files that they've uploaded that haven't expired yet
- Information available about each file: name, time uploaded


### Downloading files:
- Click a file's name to download it
- Right click file button and select 'copy link address' to get the file's link


### Uploading files (two options):
- Two options:
    - Drag and drop a file into the web browser.
    - Click the upload button to open a file browser.
- After uploading, link will automatically be copied to system clipboard


### File Expiration and Quota System
- Files remain on the server for X minutes after they're uploaded. This can be set in constants.py -> FILE_RETENTION_TIME.
- Users can upload up to X MBs of data per Y minutes starting at the time of their first upload. This can be set in server.py -> MB_UPLOAD_LIMIT. The quota reset time is set as FILE_RETENTION_TIME.
- After a user reaches their upload limit, they are prevented from uploading any more data until their quota is reset.

### Deploying With Apache and WSGI on Ubuntu
- Install Apache and WSGI
	$ sudo apt-get install libapache2-mod-wsgi 
- Enable WSGI
	$ sudo a2enmod wsgi 
- Install dependencies as usual
- Modify the VirtualHost conf file found here
	https://www.digitalocean.com/community/articles/how-to-deploy-a-flask-application-on-an-ubuntu-vps

** Make sure you change the datastore path in src/constants.py to a directory that Apache has access to and owns, such as /var/www/datastore. Otherwise, you'll see permission denied errors in the log when trying to upload and file operations won't work properly.
