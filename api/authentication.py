import json

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse

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
            data = {"error": "null", "data": {"authenticated": "true"}}
        else:
            data = {"error": "login failed, user inactive", "data": \
                    {"authenticated": "false"}}
    else:
        data = {"error": "login failed, incorrect login info", "data": \
                {"authenticated": "false"}}
    data = json.dumps(data)
    return HttpResponse(data,mimetype='application/json')