from bottle import redirect, request, route, static_file

from template  import render
from fileutils import get_file_info

from   .          import *
print(FILE_RETENTION_TIME)



@route('/')
def route_root():
    return render('index.jade', {'files': get_file_info()})

@route('/download/<filepath:path>')
def download_file(filepath):
    return static_file(filepath, root=FILE_RETENTION_TIME)

@route('/upload', method='POST')
def upload_runner():
    data   = request.files.get('upload')
    thread = threading.Thread(target=upload_file, args=[data])
    thread.daemon = True
    thread.start()
    return redirect('/')

@route('/debug/list_files')
def list_files():
    return [f for f
        in listdir(datastore_path)
        if isfile(join(datastore_path, f))]

@route('/debug/path')
def print_path():
    return datastore_path


# Static files
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
