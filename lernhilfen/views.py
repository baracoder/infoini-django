# coding=utf-8
from django.shortcuts import render_to_response
from infoini.lernhilfen import models, forms
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf



def index(request):
    # übersicht mit filteroptionen anzeigen
    filterset = forms.LernhilfenFilterSet(request.GET or None)
    return render_to_response('lernhilfen/index.html', {
        'filter':filterset
        })

@csrf_protect
def upload(request):
    uploadform = forms.LernhilfenUpload(request.POST or None, request.FILES or None)
    if request.POST and uploadform.is_valid():
        uploadform.save()


    c = {
        'uploadform':uploadform
    }
    c.update(csrf(request))
    return render_to_response('lernhilfen/upload.html', c)

def sichten(request):
    # muss in gruppe FSR oder Helper sein
    # alle ungesichteten dateinen anzeigen
    # option zum sichten anbieten
    pass

