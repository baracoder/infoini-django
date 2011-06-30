# coding=utf-8
from django.shortcuts import render_to_response
from infoini.lernhilfen import models, forms


def index(request):
    # übersicht mit filteroptionen anzeigen
    filterset = forms.LernhilfenFilterSet(request.GET or None)
    return render_to_response('lernhilfen/index.html', {
        'filter':filterset
        })

def upload(request):
    # todo
    return False

def sichten(request):
    # muss in gruppe FSR oder Helper sein
    # alle ungesichteten dateinen anzeigen
    # option zum sichten anbieten
    pass

