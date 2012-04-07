# coding=utf-8
from infoini.lernhilfen import models, forms
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from infoini.shortcuts import render_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from django.core.files import File
from django.conf import settings

import json

import os, random

@csrf_protect
@login_required
def index(request):
    filterset = forms.LernhilfenFilterSet()
    c = {
        'filter':filterset,
        'q':request.GET.urlencode()
    }
    return render_response(request,'lernhilfen/index.html',c)

def ajax_get(request):
    # anzahl lernhilfen pro seite
    onpage = 10

    if request.GET and request.GET.has_key('semester'):
        filterset = forms.LernhilfenFilterSet(request.GET)
    else:
        filterset = forms.LernhilfenFilterSet()

    offset = 0
    if request.GET and request.GET.has_key('offset'):
        offset = int(request.GET['offset'])
    list_strt = offset * onpage
    list_end  = (offset+1) * onpage

    qs = filterset.qs
    if request.GET.has_key('ungesichtet'):
        qs = qs.filter(gesichtet=False)
    if not request.user.is_staff:
        qs = qs.filter(gesichtet=True)

    qs_page = qs[list_strt:list_end]

    has_prev = offset>0
    has_next = len(qs)>list_end

    fields = [ 'id', 'name', 'endung', 'art', 'modul', 'dozent',
                'studiengang', 'semester', 'gesichtet']
    rows = []
    for r in qs_page:
        row = {}
        for f in fields:
            row[f]=unicode(r.__getattribute__(f))
            # datei braucht sonder bhandlung
            row['datei'] = unicode(r.datei.url)
        rows.append(row)
    resp = {'has_prev':has_prev,
            'has_next':has_next,
            'rows':rows,
            }
    return HttpResponse(json.dumps(resp), mimetype="application/json")

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
    basepath =  os.path.join(settings.MEDIA_ROOT,'lernhilfen_archiv')

    if request.POST.has_key('datei'):
        randomfile_url = request.POST['datei']
    else:
        try:
            randomfile = get_random_file(basepath)
            randomfile_url = os.path.relpath(randomfile,settings.MEDIA_ROOT)
        except IndexError:
           return HttpResponse("keine unsortierten dateien gefunden",status=500)


    sort_form = forms.LernhilfenSort(request.POST or None)
    if request.POST and sort_form.is_valid():
        l = sort_form.save(commit=False)
        filename = request.POST['datei']

        if '..' in filename or filename.startswith('/'):
            return HttpResponse(status=403)

        filename = os.path.join(settings.MEDIA_ROOT,filename)

        l.datei.save(models.get_full_path(l,filename),File(open(filename)))
        l.gesichtet=True
        l.save()
        os.remove(filename)
        messages.success(request,'Lernhilfe gespeichert')
        return HttpResponseRedirect('/lernhilfen/sort/')


    c = {
        'sort_form':sort_form,
        'src':randomfile_url,
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

