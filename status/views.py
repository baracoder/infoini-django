# coding=utf-8
from django.shortcuts import render_to_response
from status import ist_offen, potinfo


def status(request):
    return render_to_response('status.xml',{'status':ist_offen(), 'cafepots':potinfo()}, mimetype='text/xml; charset=utf-8')

