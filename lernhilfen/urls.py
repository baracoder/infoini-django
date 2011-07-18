from django.conf.urls.defaults import *


urlpatterns = patterns('infoini.lernhilfen.views',
    ( r'^$', 'index'),
    ( r'^upload/$', 'upload'),
)
