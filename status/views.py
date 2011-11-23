# coding=utf-8
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page

from status import ist_offen, potinfo


@cache_page(2) # für 2 sekunden cachen um spitzen besser abfangen zu können
def status(request):
    return render_to_response('status.xml',{'status':ist_offen(), 'cafepots':potinfo()}, mimetype='text/xml; charset=utf-8')

@cache_page(2) # für 2 sekunden cachen um spitzen besser abfangen zu können
def status_html(request):
    return render_to_response('status.html',{'ist_offen':ist_offen(), 'cafepots':potinfo()})


