from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from views import RegistrationView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('DryIce.views',
    # Examples:
    # url(r'^$', 'DryIce.views.home', name='home'),
    # url(r'^DryIce/', include('DryIce.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

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

urlpatterns += patterns('DryIce.api',
    url(r'^api/home/$', 'home_data', name='home_data'),
    url(r'^api/route_file/(?P<ez_link>\w+)/$', 'route_file_data', name='route_file_data')
)