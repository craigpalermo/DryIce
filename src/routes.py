from flask      import Flask, render_template
from threading  import Thread

from template   import render
from fileutils import get_file_info, list_files, upload_file

from converter import RegexConverter
from constants import *
from server     import app

app.url_map.converters['regex'] = RegexConverter

# Render pages
@app.route('/')
def route_root():
    return render_template('index.jade', {'files': get_file_info()})


# Upload and download files
@app.route('/download/<path:filename>')
def download_file(filepath):
    return send_from_directory(PATH_DATASTORE, filename)

@app.route('/upload')
def upload_runner():
    if request.method == 'POST':
        f      = request.files.get('upload')
        thread = Thread(target=upload_file, args=[data])
        thread.daemon = True
        thread.start()
    return redirect('/')


# Debug
@app.route('/debug/list_files')
def debug_list_files():
    return map(lambda f: f+' ', list_files())

# Static assets
@app.route('/<regex(".*\.js"):filename>/')
def javascripts(filename):
    return url_for('static', filename=filename)

@app.route('/<regex(".*\.css>"):filename>/')
def stylesheets(filename):
    return url_for('static', filename=filename) 

@app.route('/<regex(".*\.(jpg|png|gif|ico)"):filename>/')
def images(filename):
    return url_for('static', filename=filename)

@app.route('/<regex(".*\.(eot|ttf|woff|svg)"):filename>/')
def fonts(filename):
    return url_for('static', filename=filename)
