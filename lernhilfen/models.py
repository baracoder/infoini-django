# coding=utf-8
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

import os
import mimetypes
mimetypes.init()


class Typ(models.Model):
    class Meta:
        verbose_name="Typ"
        verbose_name_plural="Typen"
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

    def get_path(self):
        return slugify(self.name)

class Fach(models.Model):
    class Meta:
        verbose_name="Fach"
        verbose_name_plural="Fächer"
    name = models.CharField(max_length=100)
    kurzname = models.CharField(max_length=10)

    def __unicode__(self):
        return self.kurzname + ' (' + self.name + ')'

    def get_path(self):
        return slugify(self.kurzname)

class Studiengang(models.Model):
    class Meta:
        verbose_name="Studiengang"
        verbose_name_plural="Studiengänge"
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
    def get_path(self):
        return slugify(self.name)

# hilfsmethode
def get_path(self,fname=None):
    if fname:
        self.endung = os.path.splitext(fname)[1].lower()
    return os.path.join(
        'lernhilfen',
        self.fachrichtung.get_path(),
        self.fach.get_path(),
        self.get_filename() + self.endung)


class Lernhilfe(models.Model):
    class Meta:
        verbose_name="Lernhilfe"
        verbose_name_plural="Lernhilfen"
    name = models.CharField(max_length=100)
    datei = models.FileField('Datei',upload_to=get_path)
    endung = models.CharField(max_length=40,editable=False)
    typ = models.ForeignKey('Typ')
    fach = models.ForeignKey('Fach')
    fachrichtung = models.ForeignKey('Studiengang')
    gesichtet = models.BooleanField(default=False)

    # methode
    get_path=get_path

    def __unicode__(self):
        return self.name

    def get_filename(self):
        return slugify(self.name)


    def save(self, *args, **kwargs):
        # wenn datei bereits in db und pfad unterschiedlich: verschieben
        if self.id:
            old_path = self.datei.name
            new_path = self.get_path()
            if old_path != new_path:
                self._file_move(
                    os.path.join(settings.MEDIA_ROOT,old_path),
                    os.path.join(settings.MEDIA_ROOT,new_path))
                self.datei.name=new_path
        super(Lernhilfe, self).save()


    def delete(self, *args, **kwargs):
        self._file_delete()
        super(Lernhilfe, self).delete()


    def _create_folder_if_not_exists(self):
        d = os.path.dirname(self.get_path())
        if not os.path.exists(d):
            os.makedirs(d)

    def _file_move(self, old, new):
        self._create_folder_if_not_exists()
        if os.path.exists(new): raise ValidationError('Datei bereits vorhanden')
        os.rename(old,new)


    def _file_delete(self):
        p = os.path.join(settings.MEDIA_ROOT, self.get_path())
        try:
            os.remove(p)
            return True
        except os.error:
            return False

admin.site.register(Typ)
admin.site.register(Fach)
admin.site.register(Studiengang)
admin.site.register(Lernhilfe)
