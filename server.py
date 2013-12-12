from bottle import route, run, static_file
from os import listdir
from os.path import isfile, join
from os import walk

import os


path = os.path.dirname(os.path.realpath(__file__))
datastore_path = path + '/datastore'


@route('/')
def route_root():
    return static_file("index.html", root=path + '/public')

@route('/download/<filepath:path>')
def download_file(filepath):
    '''
    Download the file whose path is in the URL
    '''
    return static_file(filepath, root=datastore_path)

@route('/upload', method='POST')
def upload_file():
    '''
    Upload the file that the user enters in the form
    '''
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    upload.save(datastore_path)
    return 'Success!'

@route('/list')
def list_files():
    '''
    Lists all the files in the datastore
    '''
    files = []
    for (dirpath, dirnames, filenames) in walk(datastore_path):
        files.extend(filenames)

    return files

@route('/path')
def print_path():
    '''
    Prints the absolute path of the datastore directory, 
    FOR DEBUG USE ONLY
    '''
    return datastore_path


 # Static Routes
@route('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root=path + '/public')

@route('/<filename:re:.*\.css>')
def stylesheets(filename):
    print(filename)
    return static_file(filename, root=path + '/public')

@route('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root=path + '/public')

@route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root=path + '/public')


run(host='localhost', port=8080, debug=True)
