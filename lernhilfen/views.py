# coding=utf-8
from infoini.lernhilfen import models, forms
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from infoini.shortcuts import render_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect


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
        return HttpResponseRedirect('/lernhilfen/')

    c = {
        'uploadform':uploadform
    }
    c.update(csrf(request))
    return render_response(request,'lernhilfen/upload.html', c)

def sichten(request,id,params):
    if request.user.is_staff:
        l = models.Lernhilfe.objects.get(pk=id)
        l.gesichtet = True
        l.save()
        return HttpResponseRedirect('/lernhilfen/?'+params)
    else:
        return HttpResponseForbidden('Nicht gestattet')

