import base64
import hmac, hashlib
import uuid, json

from random_words  import RandomWords
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.http import HttpResponse

from DryIce.settings import FILE_RETENTION_TIME, MB_UPLOAD_LIMIT, BUCKET, \
                            SECRET_ACCESS_KEY, MAX_CONTENT_LENGTH
from DryIce.models import UserProfile

def get_session_id(request):
    if request.user.is_authenticated():
        profile = UserProfile.objects.get(user=request.user)
        return profile.uuid
    else:
        # set uuid in session
        if not 'session_id' in request.session:
            request.session['session_id'] = str(uuid.uuid1())
        return request.session.get('session_id')
        
# S3 Storage Setup
def generate_upload_form(request):
    session_id = request.POST.get('session_id', 0)
    expire_time = request.POST.get('expire_time', FILE_RETENTION_TIME)
    
    policy = """
    {"expiration": "%(expires)s",
        "conditions": [ 
            {"bucket": "%(bucket)s"}, 
            ["starts-with", "$key", ""],
            {"acl": "%(acl)s"},
            {"success_action_redirect": "%(success_redirect)s"},
            ["starts-with", "$Content-Type", ""],
            ["content-length-range", 0, %(length_range)s],
            {"x-amz-meta-session_id": "%(session_id)s"},
            {"x-amz-meta-expire_time": "%(expire_time)s"},
        ]
    }
    """
    
    policy = policy%{
        "expires":"2015-01-01T00:00:00Z",
        "bucket": BUCKET,
        "acl": "public-read",
        "success_redirect": "/",
        "length_range": MAX_CONTENT_LENGTH,
        "session_id": session_id,
        "expire_time": expire_time
    }

    policy = base64.b64encode(policy)
    signature = base64.b64encode(hmac.new(SECRET_ACCESS_KEY, policy, hashlib.sha1).digest())
    temp = {"policy":policy, "signature":signature}
    data = {"error": "null", "data": temp}
    return HttpResponse(json.dumps(data), mimetype='application/json') 