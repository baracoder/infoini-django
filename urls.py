from django.conf.urls.defaults import *
from infoini import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^status/$', 'status.views.status_xml'),
    (r'^status.xml$', 'status.views.status_xml'),
    (r'^status.html$', 'status.views.status_html'),
    (r'^status.json$', 'status.views.status_json'),
    (r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^lernhilfen/', include('lernhilfen.urls')),

    # Benutzerlogin/logout
    (r'^user/login/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}),
    (r'^user/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'user/logout.html'}),


    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
)
