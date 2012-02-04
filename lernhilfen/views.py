# coding=utf-8
from infoini.lernhilfen import models, forms
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from infoini.shortcuts import render_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from django.core.files import File

import os, random

@csrf_protect
@login_required
def index(request):
    if request.GET and request.GET.has_key('semester'):
        filterset = forms.LernhilfenFilterSet(request.GET)
    else:
        filterset = forms.LernhilfenFilterSet()

    l = filterset.qs
    if request.GET.has_key('ungesichtet'):
        l = l.filter(gesichtet=False)
    if not request.user.is_staff:
        l = l.filter(gesichtet=True)

    c = {
        'filter':filterset,
        'l':l,
        'q':request.GET.urlencode()
    }
    c.update(csrf(request))
    return render_response(request,'lernhilfen/index.html', c)

@csrf_protect
@login_required
def upload(request):
    uploadform = forms.LernhilfenUpload(request.POST or None, request.FILES or None)
    if request.POST and uploadform.is_valid():
        uploadform.save()
        messages.success(request,'Lernhilfe hochgeladen')
        return HttpResponseRedirect('/lernhilfen/')

    c = {
        'uploadform':uploadform
    }
    c.update(csrf(request))
    return render_response(request,'lernhilfen/upload.html', c)

@csrf_protect
@login_required
def sort(request):
    basepath = 'media/lernhilfen_archiv'
    randomfile = get_random_file(basepath)

    sort_form = forms.LernhilfenSort(request.POST or None)
    if request.POST and sort_form.is_valid():
        l = sort_form.save(commit=False)
        filename = request.POST['datei']

        if '..' in filename or filename.startswith('/'):
            return HttpResponse(status=403)

        l.datei.save(models.get_full_path(l,filename),File(open(filename)))
        l.gesichtet=True
        l.save()
        os.remove(filename)
        messages.success(request,'Lernhilfe gespeichert')
        return HttpResponseRedirect('/lernhilfen/sort/')

    c = {
        'sort_form':sort_form,
        'src':randomfile,
    }
    c.update(csrf(request))
    return render_response(request,'lernhilfen/sort.html', c)

def get_random_file(start_path,max_tries=20):
    path = start_path
    tries = 0

    while not os.path.isfile(path):
        try:
            path = path + '/'+ random.choice(os.listdir(path))
        except (Exception):
            # etwas schief gelaufen? neustarten!
            path = start_path
            tries +=1
            if tries >= max_tries: raise
    return path

def sichten(request,id,params):
    if request.user.is_staff:
        l = models.Lernhilfe.objects.get(pk=id)
        l.gesichtet = True
        l.save()
        messages.success(request,'%s gesichtet' % l.name)
        return HttpResponseRedirect('/lernhilfen/?'+params)
    else:
        return HttpResponseForbidden('Nicht gestattet')

