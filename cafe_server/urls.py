from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to


urlpatterns = patterns('cafe_server.views',
    (r'^status/$', 'status_xml'),
    (r'^status.xml$', 'status_xml'),
    (r'^status.html$', 'status_html'),
    (r'^status.json$', 'status_json'),

    # alte url umleitung
    (r'^tuer/$', redirect_to, {'url': '/status.html'}),
)
