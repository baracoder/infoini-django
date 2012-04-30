from django.conf.urls.defaults import *


urlpatterns = patterns('infoini.lernhilfen.views',
    ( r'^$', 'index'),
    ( r'^upload/$', 'upload'),
    ( r'^get/$', 'ajax_get'),
    ( r'^sort/$', 'sort'),
    ( r'^archiv/$', 'sort'),
    (r'^sichten/(?P<id>\d+)/(?P<params>.*)$', 'sichten'),
)
