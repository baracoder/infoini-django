# coding=utf-8
from django.shortcuts import render_to_response
from tuer import ist_offen


def index(request):
    if ist_offen():
        status = "Tür offen"
    else:
        status = "Tür geschlossen"

    return render_to_response('tuer/index.html',{'status':status})

def status(request):
    return render_to_response('status.xml',{'status':ist_offen()}, mimetype='text/xml; charset=utf-8')

