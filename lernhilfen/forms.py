import django_filters
from django.forms import ModelForm

from infoini.lernhilfen import models

class LernhilfenFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.Lernhilfe
        fields = [ 'studiengang','modul','dozent','semester','art']


class LernhilfenUpload(ModelForm):
    class Meta:
        model = models.Lernhilfe
        exclude = ('gesichtet',)

class LernhilfenSort(ModelForm):
    class Meta:
        model = models.Lernhilfe
        exclude = ('gesichtet','datei',)


