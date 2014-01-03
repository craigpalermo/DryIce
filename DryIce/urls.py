from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from views import RegistrationView
from settings import SITE_ROOT

urlpatterns = patterns('',
    url(r'^partials/(?P<path>.*)$', 'django.views.static.serve', \
            {'document_root': SITE_ROOT + '/static/partials/'}),
)

urlpatterns += patterns('DryIce.views',
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'home', name='home'),
    url(r'^disclaimer/$', TemplateView.as_view(template_name='disclaimer.html')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^clear_session/$', 'clear_session', name='clear_session'),
    url(r'^(?P<ez_link>\w+)/$', 'route_file', name='route_file'),
    
    url(r'^users/sign_up/$', RegistrationView.as_view(), name='sign_up'),
    url(r'^users/login/$', 'login_user', name='login'),
    url(r'^users/logout/$', 'logout_view', name='logout'),
)

# API data views
urlpatterns += patterns('api.views',
    url(r'^api/home/$', 'home_data', name='home_data'),
    url(r'^api/route_file/(?P<ez_link>\w+)/$', 'route_file_data', name='route_file_data'),
    url(r'^api/register/$', 'register_data', name='register_data'),
    url(r'^api/base/$', 'base_data', name='base_data'),
)

# Authentication
urlpatterns += patterns('api.authentication',
    url(r'^api/login/$', 'login_user', name='login_data')
)
