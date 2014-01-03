import json

from django.http import HttpResponse
from django.core.context_processors import csrf

from redis import Redis
from datetime import datetime, timedelta

from DryIce.utils.file_utils import get_file_info, delete_session_keys, \
                                    setup_bucket, generate_ez_link
from DryIce.utils.session_utils import generate_upload_form, get_session_id
from DryIce.settings import REDIS_ADDRESS, MAX_CONTENT_LENGTH, \
                            FILE_RETENTION_TIME, BUCKET, ACCESS_KEY

# Setup connection to redis server
r_server = Redis(REDIS_ADDRESS)


def home_data(request):
    files = []
    session_id = get_session_id(request)
    
    temp = get_file_info(session_id)
    form_dict = generate_upload_form(session_id)
    
    # pick out which files were uploaded from the current session
    for f in temp:
        print f
        f_name = f.get('name')
        f['expire_time'] = str(f['created'] + \
                            timedelta(minutes=FILE_RETENTION_TIME))
        f['created'] = str(f['created'])
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
                    'files': files,
                    'size_limit': MAX_CONTENT_LENGTH,
                    'session_id': session_id,
                    'AWSAccessKeyId': ACCESS_KEY,
                    'bucket': BUCKET
                    }

    template_data.update(form_dict)
    template_data = {"error": "null", "data": template_data}
    data = json.dumps(template_data)
    return HttpResponse(data,mimetype='application/json')
    
def route_file_data(request, ez_link):
    bucket = setup_bucket()
    filename = r_server.get(ez_link)
    data = {}
    if filename != None:
        key = bucket.new_key(filename)
        url = key.generate_url(expires_in=(FILE_RETENTION_TIME * 60),query_auth=False, force_http=True)
        filename = filename[37:] # strip folder prefix
        data = {"error": "null", "data": {'filename': filename, 'url': url}}
    else:
        message = "That EZLink didn't match any files. Verify correct spelling and capitalization, then try again."
        data = {"error": "file not found", "data": "null"}
    data = json.dumps(data)
    return HttpResponse(data,mimetype='application/json')

def register_data(request):
    for x in csrf(request).viewvalues():
        csrf_value = x
    data = {
            "csrf_token": str(csrf_value)
            }
    return HttpResponse(json.dumps(data),mimetype='application/json')

def base_data(request):
    for x in csrf(request).viewvalues():
        csrf_value = x
    data = {
            "csrf_token": str(csrf_value),
            "user_authenticated": str(request.user.is_authenticated()).lower(),
            }
    return HttpResponse(json.dumps(data),mimetype='application/json')