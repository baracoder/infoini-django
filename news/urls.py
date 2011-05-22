from django.conf.urls.defaults import *

from news.models import News
from tuer import ist_offen
from django.views.generic.list_detail import object_list, object_detail

info_dict = {
    'queryset': News.objects.all(),
    'extra_context': {'ist_offen':ist_offen()}
}
list_dict = info_dict.copy()
list_dict['paginate_by']=5



urlpatterns = patterns('',
    ( r'^$', object_list, list_dict),
    ( r'page/(?P<page>[0-9]+)/$', object_list, info_dict),
    ( r'(?P<object_id>\d+).+/$', object_detail, info_dict),
)
