from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from views import RegistrationView
from settings import SITE_ROOT

urlpatterns = patterns('',
    url(r'^api/upload-form/$', 'DryIce.utils.session_utils.generate_upload_form_data', name='upload_form'),
)

urlpatterns += patterns('DryIce.views',
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'home', name='home'),
    url(r'^disclaimer/$', TemplateView.as_view(template_name='disclaimer.html')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^clear_session/$', 'clear_session', name='clear_session'),
    url(r'^(?P<ez_link>\w+)/$', 'route_file', name='route_file'),
    url(r'^delete/(?P<filename>.+)/$', 'delete_file', name='delete'),
    
    url(r'^users/sign_up/$', RegistrationView.as_view(), name='sign_up'),
    url(r'^users/login/$', 'login_user', name='login'),
    url(r'^users/logout/$', 'logout_view', name='logout'),
)

# Partials
urlpatterns += patterns('DryIce.partial_views',
    url(r'^partials/404/$', 'not_found_view'),
    url(r'^partials/about/$', 'about_view'),
    url(r'^partials/analytics/$', 'analytics_view'),
    url(r'^partials/base/$', 'base_view'),
    url(r'^partials/disclaimer/$', 'disclaimer_view'),
    url(r'^partials/file/$', 'file_view'),
    url(r'^partials/home/$', 'index_view'),
    url(r'^partials/register/$', 'register_view'),
    url(r'^partials/pickup/$', 'pickup_view'),
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
