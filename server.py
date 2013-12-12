from bottle import route, run, static_file, request, template
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta

import os, os.path, time
import threading
import traceback
import sys


path = os.path.dirname(os.path.realpath(__file__))
datastore_path = path + '/datastore'
retention_time = 1 # in minutes


def main():
    print("Starting server")
    datetime.strptime('2013-01-01', '%Y-%m-%d')

    expire_files_thread = threading.Thread(
            target=expire_files)
    main_bottle_thread  = threading.Thread(
            target=lambda: run(host='localhost', port=8080, debug=True))

    expire_files_thread.daemon = True
    main_bottle_thread.daemon = True

    expire_files_thread.start()
    main_bottle_thread.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit()


@route('/')
def route_root():
    return template('public/index.html', files=list_files())

@route('/download/<filepath:path>')
def download_file(filepath):
    return static_file(filepath, root=datastore_path)

@route('/upload', method='POST')
def upload_file():
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    upload.save(datastore_path)
    return 'Success!'


@route('/debug/list_files')
def list_files():
    return [f for f
            in listdir(datastore_path)
            if isfile(join(datastore_path, f))]

@route('/debug/path')
def print_path():
    return datastore_path


def expire_files():
    '''
    Removes from the datastore directory all files that have modified
    time older than retention_time
    '''
    while(True):
        files = list_files()
        for f in files:
            try:
                temp = time.ctime(os.path.getmtime(datastore_path + '/' + f))
                age = datetime.now() - datetime.strptime(temp, "%a %b %d %H:%M:%S %Y")
                if age > timedelta(minutes=retention_time):
                    os.remove(datastore_path + '/' + f)
            except:
                print("error statting files - " + traceback.format_exc())
        time.sleep(60)


# Static Routes
@route('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root=path + '/public')
@route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root=path + '/public')
@route('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root=path + '/public')
@route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root=path + '/public')


if __name__ == "__main__":
    main()
