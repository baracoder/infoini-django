# coding=utf-8
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.http import HttpResponse

import json

from . import get_all


@cache_page(2) # für 2 sekunden cachen um spitzen besser abfangen zu können
def status_xml(request):
    return render_to_response('cafe_server/status.xml',get_all(), mimetype='text/xml; charset=utf-8')

@cache_page(2)
def status_json(request):
    return HttpResponse(json.dumps(get_all()), mimetype="application/json")


@cache_page(2)
def status_html(request):
    return render_to_response('cafe_server/status.html',get_all())


