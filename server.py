from bottle import route, run, static_file
import os


path = os.path.dirname(os.path.realpath(__file__))


@route('/')
def route_root():
    return static_file("index.html", root=path + '/public')

@route('/download/<filepath:path>')
def download_file(filepath):
    return static_file(filepath, root=path + '/datastore')


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
