from django.conf.urls.defaults import *


urlpatterns = patterns('cafe_server.views',
    (r'^status/$', 'status_xml'),
    (r'^status.xml$', 'status_xml'),
    (r'^status.html$', 'status_html'),
    (r'^status.json$', 'status_json'),
)
