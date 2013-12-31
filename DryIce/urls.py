from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('DryIce.views',
    # Examples:
    # url(r'^$', 'DryIce.views.home', name='home'),
    # url(r'^DryIce/', include('DryIce.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'home', name='home'),
    url(r'^disclaimer/$', TemplateView.as_view(template_name='disclaimer.html')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^clear_session/$', 'clear_session', name='clear_session'),
    url(r'^(?P<ez_link>\w+)/$', 'route_file', name='route_file'),
)
