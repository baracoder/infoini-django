import django_filters

from infoini.lernhilfen import models

class LernhilfenFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.Lernhilfe
        fields = [ 'studiengang','modul','dozent','semester','art']
