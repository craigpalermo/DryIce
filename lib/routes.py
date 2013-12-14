from bottle     import redirect, request, route, static_file
from threading  import Thread

from template   import render
from .fileutils import get_file_info, list_files, upload_file

from .constants import *


def def_routes():
    # Render pages
    @route('/')
    def route_root():
        return render('index.jade', {'files': get_file_info()})


    # Upload and download files
    @route('/download/<filepath:path>')
    def download_file(filepath):
        return static_file(filepath, root=FILE_RETENTION_TIME)

    @route('/upload', method='POST')
    def upload_runner():
        data   = request.files.get('upload')
        thread = Thread(target=upload_file, args=[data])
        thread.daemon = True
        thread.start()
        return redirect('/')


    # Debug
    @route('/debug/list_files')
    def debug_list_files():
        return map(lambda f: f+' ', list_files())


    # Static assets
    @route('/<filename:re:.*\.js>')
    def javascripts(filename):
        return static_file(filename, root=PATH_ROOT + '/public')

    @route('/<filename:re:.*\.css>')
    def stylesheets(filename):
        return static_file(filename, root=PATH_ROOT  + '/public')

    @route('/<filename:re:.*\.(jpg|png|gif|ico)>')
    def images(filename):
        return static_file(filename, root=PATH_ROOT  + '/public')

    @route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
    def fonts(filename):
        return static_file(filename, root=PATH_ROOT  + '/public')
