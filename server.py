from bottle   import route, run, static_file, request
from os       import listdir
from os.path  import isfile, join
from datetime import datetime, timedelta

import os, os.path, time
import threading
import traceback
import sys

from lib.template import render


path           = os.path.dirname(os.path.realpath(__file__))
datastore_path = path + '/datastore'
retention_time = 10 # in minutes


def main():
    datetime.strptime('2013-01-01', '%Y-%m-%d')

    expire_files_thread = threading.Thread(
            target=expire_files)
    main_bottle_thread  = threading.Thread(
            target=lambda: run(host='0.0.0.0', port=8080, debug=True))

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
    return render('index.jade', {'files': get_file_info()})

@route('/download/<filepath:path>')
def download_file(filepath):
    return static_file(filepath, root=datastore_path)

@route('/upload', method='POST')
def upload_runner():
    data = request.files.get('upload')
    thread = threading.Thread(target=upload_file, args=[data])
    thread.daemon = True
    thread.start()
    return route_root()

def upload_file(data):
    name, ext = os.path.splitext(data.filename)
    # data.save(datastore_path)
    
    raw = data.file.read() # small files =.=
    filename = data.filename
    with open(datastore_path + '/' + filename, 'w') as f:
        f.write(raw)

@route('/debug/list_files')
def list_files():
    return [f for f
        in listdir(datastore_path)
        if isfile(join(datastore_path, f))]

def get_file_info():
    files = []
    try:
        for f in list_files():
            temp_time = time.ctime(os.path.getmtime(datastore_path + '/' + f))
            file_time = datetime.strptime(temp_time, "%a %b %d %H:%M:%S %Y")
            files.append({'name': f, 'created': file_time})
    except: pass
    return files

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
