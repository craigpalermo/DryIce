import sys, time
import base64
import hmac, hashlib

from flask         import Flask, send_from_directory, request, redirect, \
                            url_for, session, render_template
from werkzeug.exceptions import RequestEntityTooLarge
from time          import sleep
from threading     import Thread
from time          import mktime

from fileutils     import *
from converter     import RegexConverter
from template      import render
from constants     import *

# Global Variables
MB_UPLOAD_LIMIT = 512
count = 0

# Flask Configuration
app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.config['UPLOAD_FOLDER'] = PATH_DATASTORE
app.config['MAX_CONTENT_LENGTH'] = MB_UPLOAD_LIMIT * 1024 * 1024 
app.secret_key = '8s9fs9fs09dfi9324s'

# S3 Storage Setup
def generate_upload_form():
    policy = """
    {"expiration": "%(expires)s",
        "conditions": [ 
            {"bucket": "%(bucket)s"}, 
            ["starts-with", "$key", ""],
            {"acl": "%(acl)s"},
            {"success_action_redirect": "%(success_redirect)s"},
            ["starts-with", "$Content-Type", ""],
            ["content-length-range", 0, %(length_range)s]
        ]
    }
    """
    policy = policy%{
        "expires":"2015-01-01T00:00:00Z",
        "bucket": BUCKET,
        "acl": "public-read",
        "success_redirect": "/",
        "length_range": app.config['MAX_CONTENT_LENGTH']
    }

    policy = base64.b64encode(policy)
    signature = base64.b64encode(hmac.new(SECRET_ACCESS_KEY, policy, hashlib.sha1).digest())
    return {'policy':policy, 'signature':signature}

# Routes ------------------------------------------------------------------
@app.route('/')
def route_root():
    quota_remaining = MB_UPLOAD_LIMIT - session.get('mb_used', 0)
    temp = get_file_info()
    files = []
   
    update_reset_time()
    
    # pick out which files were uploaded from the current session
    for f in temp:
        #if f['name'] in session.get('uploads', []):
        f['expire_time'] = f['created'] + \
                            timedelta(minutes=FILE_RETENTION_TIME)
        files.append(f)
    
    template_data = {
                    'files': files, \
                    'size_limit': app.config['MAX_CONTENT_LENGTH'], \
                    'quota_left': quota_remaining, \
                    'reset_time': session.get('reset_time'), \
                    'quota_reached': session.get('quota_reached', 'false')
                    }

    temp = generate_upload_form()
    template_data.update(temp)

    return render('index.jade', template_data)

@app.route('/disclaimer/')
def route_disclaimer():
    return render('disclaimer.html')

@app.route('/about/')
def route_about():
    return render('about.html')

@app.errorhandler(404)
def page_not_found(e):
	return render('404.html')

@app.route('/file/<path:filename>/')
def route_file(filename):
    bucket = setup_bucket()
    key = bucket.new_key(filename)
    url = key.generate_url(expires_in=(FILE_RETENTION_TIME * 60),query_auth=False, force_http=True)
    template_data = {'filename': filename, 'url': url}
    return render('file.html', template_data)

# Upload and download files
# In production, download_file should be removed and add this line to apache.conf:
# $ alias /download/ /var/www/datastore/
'''
@app.route('/download/<path:filename>/')
def download_file(filename):
    return send_from_directory(PATH_DATASTORE, filename)
'''

@app.route('/upload/', methods=['GET', 'POST'])
def upload_runner():
    if request.method == 'POST':
        try:
            file = request.files.get('upload')
            if file and session.get('quota_reached', 'false') != 'true' \
                    and MB_UPLOAD_LIMIT - (session.get('mb_used', 0) \
                        + file.content_length) >= 0:
                filename = secure_filename(file.filename)
               
                # if filename exists, prepend unique number to new name
                files = get_file_info()
                for f in files:
                    if filename == f['name']:
                        filename = str(counter()) + filename
                        break

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], \
                            filename))
                size = os.path.getsize(app.config['UPLOAD_FOLDER'] + \
                                        '/' + filename)
                update_session((size/1024/1024), filename)
        except RequestEntityTooLarge:
            print "File size too large"
        except:
            print traceback.format_exc()
    return redirect('/')


# Other Functions --------------------------------------------------------
def update_session(filesize, filename):
    '''
    Adds the filesize (in MB) to the user's value in ip_list and adds the
    filename to the user's list of uploads
    '''
    if 'mb_used' in session:
        session['mb_used'] += filesize
    else: # initialize mb_used
        session['mb_used'] = filesize
    
    if 'uploads' in session:
        session['uploads'].append(filename)
    else:
        session['uploads'] = [filename]
    
    update_reset_time()

def update_reset_time():
    '''
    Updates the session's reset time and quota when the current time
    becomes greater than reset time
    '''
    temp_reset_time =  datetime.now() + \
                       timedelta(minutes=FILE_RETENTION_TIME)
    
    if 'reset_time' in session:
        # time's up, reset the time
        if datetime.now() > session['reset_time']:
            session['reset_time'] = temp_reset_time
            session['quota_reached'] = 'false'
            session['mb_used'] = 0
        else: # time not up yet, check to see if quota reached
            if session.get('mb_used', 0) > MB_UPLOAD_LIMIT:
                session['quota_reached'] = 'true'
    else: # initialize the reset time
        session['reset_time'] = temp_reset_time

def counter():
    '''
    Provides a unique number used to differentiate filenames to avoid
    overwriting files with duplicate names
    '''
    global count
    temp = count
    count += 1
    return temp

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


# Server ------------------------------------------------------------------
def main():
    # dummy call b/c strptime has thread-related bug
    datetime.strptime('2013-01-01', '%Y-%m-%d')

    # start the server
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
