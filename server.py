from bottle import route, static_file, template, request, run

from os import listdir
from os.path import realpath, dirname, splitext, join, isfile


path           = dirname(realpath(__file__))
datastore_path = path + '/datastore'


@route('/')
def route_root():
    return template('public/index.html', files=list_files())

@route('/download/<filepath:path>')
def download_file(filepath):
    return static_file(filepath, root=datastore_path)

@route('/upload', method='POST')
def upload_file():
    upload = request.files.get('upload')
    name, ext = splitext(upload.filename)
    upload.save(datastore_path)
    return 'Success!'

@route('/debug-list_files')
def list_files():
    return [f for f
            in listdir(datastore_path)
            if isfile(join(datastore_path, f))]

@route('/debug-print_path')
def print_path():
    # FIXME: debug
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


run(host='localhost', port=8080, debug=True, reloader=True)
