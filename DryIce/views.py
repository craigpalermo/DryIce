import uuid

from redis import Redis
from utils.fileutils import get_file_info, delete_session_keys, setup_bucket
from utils.session_utils import update_reset_time, generate_upload_form, \
                                generate_ez_link
from DryIce.settings import REDIS_ADDRESS, MAX_CONTENT_LENGTH, FILE_RETENTION_TIME, \
                            BUCKET, ACCESS_KEY
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

# Setup connection to redis server
r_server = Redis(REDIS_ADDRESS)

def home(request):
    files = []
    update_reset_time(request)

    # set uuid in session
    if not 'session_id' in request.session:
        request.session['session_id'] = str(uuid.uuid1())
        
    session_id = request.session.get('session_id')
    temp = get_file_info(session_id)

    form_dict = generate_upload_form(session_id)

    # pick out which files were uploaded from the current session
    for f in temp:
        f_name = f.get('name')
        f['expire_time'] = f['created'] + \
                            timedelta(minutes=FILE_RETENTION_TIME)
        f['expire_time_string'] = datetime.strftime(f['expire_time'], '%Y-%m-%d %H:%M:%S')
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
                    'size_limit': MAX_CONTENT_LENGTH, \
                    'reset_time': request.session.get('reset_time'), \
                    'session_id': request.session.get('session_id'), \
                    'AWSAccessKeyId': ACCESS_KEY,
                    'bucket': BUCKET
                    }

    template_data.update(form_dict)

    return render(request, 'index.jade', template_data)

def clear_session(request):
    '''
    Delete all files linked to request's session
    '''
    delete_session_keys(request.session.get('session_id'))    
    return redirect(reverse('home'))

def page_not_found(e, message=None):
    '''
    Display 404 page with custom message
    '''
    return render('404.html', {'message': message})

def route_file(request, ez_link):
    '''
    Display page that contains filename and download link
    '''
    bucket = setup_bucket()
    filename = r_server.get(ez_link)
    if filename != None:
        key = bucket.new_key(filename)
        url = key.generate_url(expires_in=(FILE_RETENTION_TIME * 60),query_auth=False, force_http=True)
        filename = filename[37:] # strip folder prefix
        template_data = {'filename': filename, 'url': url}
        return render(request, 'file.html', template_data)
    else:
        message = "That EZLink didn't match any files. Verify correct spelling and capitalization, then try again."
        return page_not_found(None, message)