import sys, time, uuid, json
import base64
import hmac, hashlib

from flask         import Flask, send_from_directory, request, redirect, \
                            url_for, session, render_template
from werkzeug.exceptions import RequestEntityTooLarge
from time          import sleep
from threading     import Thread
from time          import mktime
from random_words  import RandomWords
from redis         import Redis

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

r_server = Redis("localhost")

# Routes ------------------------------------------------------------------
@app.route('/')
def route_root():
    files = []
    update_reset_time()

    # set uuid in session
    if not 'session_id' in session:
        session['session_id'] = str(uuid.uuid1())
        
    id = session.get('session_id')
    temp = get_file_info(id)

    form_dict = generate_upload_form(id)

    # pick out which files were uploaded from the current session
    for f in temp:
        f_name = f.get('name')
        f['expire_time'] = f['created'] + \
                            timedelta(minutes=FILE_RETENTION_TIME)
        f['nice_name'] = f.get('name')[37:] # strip folder prefix

        if not r_server.exists(f_name):
            ez_link = generate_ez_link()

            # make sure ez_link is unique
            while r_server.exists(ez_link):
                ez_link = generate_ez_link()
            
            r_server.set(f_name, ez_link)
            r_server.set(ez_link, f_name)

        f['ez_link'] = r_server.get(f_name)
        
        files.append(f)
    
    template_data = {
                    'files': files, \
                    'size_limit': app.config['MAX_CONTENT_LENGTH'], \
                    'reset_time': session.get('reset_time'), \
                    'session_id': session.get('session_id'), \
                    'AWSAccessKeyId': ACCESS_KEY
                    }

    template_data.update(form_dict)

    return render('index.jade', template_data)

@app.route('/disclaimer/')
def route_disclaimer():
    return render('disclaimer.html')

@app.route('/about/')
def route_about():
    return render('about.html')

@app.errorhandler(404)
def page_not_found(e, message=None):
    return render('404.html', {'message': message})

@app.route('/clear_session/')
def clear_session():
    delete_session_keys(session.get('session_id'))    
    return redirect(url_for('route_root'))

@app.route('/api/<action>/<int:value>/')
def route_api(action, value):
    message = {'error': 'null', 'data': 'null'}
    if action == 'size-check':
        if value > app.config['MAX_CONTENT_LENGTH']:
            message['error'] = 'File size too large'
    return json.dumps(message)

@app.route('/<path:ez_link>/')
def route_file(ez_link):
    bucket = setup_bucket()
    filename = r_server.get(ez_link)
    if filename != None:
        key = bucket.new_key(filename)
        url = key.generate_url(expires_in=(FILE_RETENTION_TIME * 60),query_auth=False, force_http=True)
        filename = filename[37:] # strip folder prefix
        template_data = {'filename': filename, 'url': url}
        return render('file.html', template_data)
    else:
        message = "That EZLink didn't match any files. Verify correct spelling and capitalization, then try again."
        return page_not_found(None, message)


# Other Functions --------------------------------------------------------
# S3 Storage Setup
def generate_upload_form(session_id):
    policy = """
    {"expiration": "%(expires)s",
        "conditions": [ 
            {"bucket": "%(bucket)s"}, 
            ["starts-with", "$key", ""],
            {"acl": "%(acl)s"},
            {"success_action_redirect": "%(success_redirect)s"},
            ["starts-with", "$Content-Type", ""],
            ["content-length-range", 0, %(length_range)s],
            {"x-amz-meta-session_id": "%(session_id)s"}
        ]
    }
    """
    policy = policy%{
        "expires":"2015-01-01T00:00:00Z",
        "bucket": BUCKET,
        "acl": "public-read",
        "success_redirect": "/",
        "length_range": app.config['MAX_CONTENT_LENGTH'],
        "session_id": session_id
    }

    policy = base64.b64encode(policy)
    signature = base64.b64encode(hmac.new(SECRET_ACCESS_KEY, policy, hashlib.sha1).digest())
    return {'policy':policy, 'signature':signature}

def generate_ez_link():
    rw = RandomWords()
    return rw.random_word().capitalize() + rw.random_word().capitalize()

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
