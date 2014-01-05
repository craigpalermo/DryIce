import uuid, json

from django.template import RequestContext
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from redis import Redis
from datetime import datetime, timedelta

from utils.file_utils import get_file_info, delete_session_keys, setup_bucket, \
                             generate_ez_link
from utils.session_utils import generate_upload_form, get_session_id
from DryIce.settings import REDIS_ADDRESS, MAX_CONTENT_LENGTH, \
                            FILE_RETENTION_TIME, BUCKET, ACCESS_KEY
from forms import UserForm
from models import UserProfile

# Setup connection to redis server
r_server = Redis(REDIS_ADDRESS)

def home(request):
    files = []
    session_id = get_session_id(request)
    
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
                    'session_id': session_id, \
                    'AWSAccessKeyId': ACCESS_KEY,
                    'bucket': BUCKET,
                    }

    template_data.update(form_dict)

    return render(request, 'index.jade', template_data, 
                  context_instance=RequestContext(request))

class RegistrationView(View):
    form_class = UserForm
    template_name = "register.jade"
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            username = cd['username']
            email = cd['email']
            password = cd['password']
            user = User.objects.create_user(username, email, password)
                            
            profile = UserProfile(user=user)
            profile.uuid = str(uuid.uuid1())
            profile.save()
            
            # log the new user in
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return redirect('home')
            
        return render(request, self.template_name, context_instance = 
                      RequestContext(request))

def login_user(request):
    '''
    Attempt to log the user in. If username and password don't match, return
    the standard error json string with error info.
    '''
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            if request.POST.has_key('remember_me'):
                request.session.set_expiry(1209600) # 2 weeks
            login(request, user)
            return redirect('/')
        else:
            message = {'error': 'login failed', 'data': 'user inactive'}
    else:
        message = {'error': 'login failed', 'data': 'incorrect login info'}
        return HttpResponse(json.dumps(message))

def logout_view(request):
    logout(request)
    return redirect('home')

def clear_session(request):
    '''
    Delete all files linked to request's session
    '''
    session_id = get_session_id(request)
    delete_session_keys(session_id)    
    return redirect(reverse('home'))

def page_not_found(request, message=None):
    '''
    Display 404 page with custom message
    '''
    return render(request, '404.html', {'message': message})

def route_file(request, ez_link):
    '''
    Display page that contains filename and download link
    '''
    bucket = setup_bucket()
    filename = r_server.get(ez_link)
    if filename != None:
        key = bucket.new_key(filename)
        url = key.generate_url(expires_in=(FILE_RETENTION_TIME * 60), \
                               query_auth=False, force_http=True)
        filename = filename[37:] # strip folder prefix
        template_data = {'filename': filename, 'url': url}
        return render(request, 'file.html', template_data)
    else:
        message = "That EZLink didn't match any files. Verify correct spelling and capitalization, then try again."
        return page_not_found(request, message)
