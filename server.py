from bottle import route, run, static_file
import os

path = os.path.dirname(os.path.realpath(__file__))

@route('/download/<filepath:path>')
def download_file(filepath):
    return static_file(filepath, root=path + '/datastore')

@route('/path')
def print_path():
    return path + '/datastore'

run(host='localhost', port=8080, debug=True)

