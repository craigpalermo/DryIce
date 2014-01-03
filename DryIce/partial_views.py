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


def not_found_view(request):
    return render(request, 'partials/404.html')


def about_view(request):
    return render(request, 'partials/about.html')


def analytics_view(request):
    return render(request, 'partials/analytics.html')


def base_view(request):
    return render(request, 'partials/base.jade')


def disclaimer_view(request):
    return render(request, 'partials/disclaimer.html')


def file_view(request):
    return render(request, 'partials/file.html')


def index_view(request):
    return render(request, 'partials/index.jade')


def register_view(request):
    return render(request, 'partials/register.jade')

