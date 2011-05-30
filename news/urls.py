from django.conf.urls.defaults import *

from news.models import News
from django.views.generic.list_detail import object_list, object_detail

info_dict = { 'queryset': News.objects.all().order_by("-pub_date") }
list_dict = info_dict.copy()
list_dict['paginate_by']=5



urlpatterns = patterns('',
    ( r'^$', object_list, list_dict),
    ( r'page/(?P<page>[0-9]+)/$', object_list, info_dict),
    ( r'(?P<object_id>\d+).+/$', object_detail, info_dict),
)
