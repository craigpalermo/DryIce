# Dropbucket
Simple way to _temporarily_ share files over the internet. No usernames or passwords, just a bucket to with files in it.


## Install and run

    $ git clone git@github.com:unscsprt/dropbucket && cd ./dropbucket
    $ pip install -r requirements.txt
    $ python server.py


## Interface
- User goes to page, sees a list of files currently stored on the server
- NAME | SIZE | UPLOAD DATE | TIME UNTIL EXPIRATION

### Downloading files:
- Click a file's name to download it
- Click `copy` button file to copy its link to the clipboard.

### Uploading files (two options):
- Drag and drop a file into the web browser.
- Click the upload button to open a file browser.
