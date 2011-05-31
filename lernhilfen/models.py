from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from os import path

class Typ(models.Model):
    name = models.CharField(max_length=100)
    def get_path(self):
        return slugify(self.name)

class Fach(models.Model):
    name = models.CharField(max_length=100)
    def get_path(self):
        return slugify(self.name)

class Fachrichtung(models.Model):
    name = models.CharField(max_length=100)
    def get_path(self):
        return slugify(self.name)


class Lernhilfe(models.Model):
    name = models.CharField(max_length=100)
    typ = models.ForeignKey('Typ')
    fach = models.ForeignKey('Fach')
    fachrichtung = models.ForeignKey('Fachrichtung')
    gesichtet = models.Boolean(default=False)


    def get_filename(self):
        return slugify(self.name)

    def get_full_path(self):
        p = path.join(
            settings.LERNHILFEN_ROOT,
            self.fachrichtung.get_path(),
            self.fach.get_path(),
            self.get_filename())
        return path.abspath(p)

    def save(self, *args, **kwargs):
        # wenn objekt bereits in db
            # objekt laden
            # wenn neuer pfad unterschiedlich zum alten:
                # datei verschieben
        super(Lernhilfe, self).save()

    def delete(self, *args, **kwargs):
        self.file_delete()
        super(Lernhilfe, self).delete()

        
    def file_save(self, f):
        p = self.get_full_path()
        # prüfen ob ordner vorhanden, ggf anlegen oder abbrechen
        # datei f speichern

    def file_delete(self):
        p = self.get_full_path()
        # p löschen
