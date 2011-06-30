# coding=utf-8
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

import os
import mimetypes
mimetypes.init()
import hashlib

class AbstractHasPath(models.Model):
    class Meta:
        abstract=True
    def __unicode__(self):
        return self.name
    def get_path(self):
        return slugify(self.__unicode__())

    def _move_all(self):
        """Alle im Bezug stehenden Lernhifen verschieben

        django erstellt automatisch einen backward
        link zum related object
        """
        for l in self.lernhilfe_set.all():
            l.move_if_path_changed()


    def save(self, *args, **kwargs):
        super(AbstractHasPath, self).save()
        # wenn objekt bereits vorhanden
        if self.id:
            self._move_all()

class Art(AbstractHasPath):
    class Meta:
        verbose_name="Art"
        verbose_name_plural="Arten"
    name = models.CharField(max_length=100)

class Modul(AbstractHasPath):
    class Meta:
        verbose_name="Modul"
        verbose_name_plural="Module"
    name = models.CharField(max_length=100)


class Studiengang(AbstractHasPath):
    class Meta:
        verbose_name="Studiengang"
        verbose_name_plural="Studiengänge"
    name = models.CharField(max_length=100)

# hilfsmethode
def get_full_path(self,fname=None):
    if fname:
        self.endung = os.path.splitext(fname)[1].lower()
    return os.path.join(
        'lernhilfen',
        self.studiengang.get_path(),
        self.modul.get_path(),
        self.dozent.get_path(),
        self.semester.get_path(),
        self.art.get_path(),
        self.get_filename() + self.endung)


class Lernhilfe(models.Model):
    class Meta:
        verbose_name="Lernhilfe"
        verbose_name_plural="Lernhilfen"
    name = models.CharField(max_length=100)
    datei = models.FileField('Datei',upload_to=get_full_path)
    endung = models.CharField(max_length=40,editable=False)
    art = models.ForeignKey('Art')
    modul = models.ForeignKey('Modul')
    dozent = models.ForeignKey('Dozent')
    studiengang = models.ForeignKey('Studiengang')
    semester = models.ForeignKey('Semester')
    gesichtet = models.BooleanField(default=False)
    md5sum = models.CharField(editable=False,max_length=36)
    pfad = models.CharField(editable=False,max_length=500)

    # methode
    get_full_path=get_full_path
    def get_full_abs_path(self):
        return os.path.join(settings.MEDIA_ROOT,self.get_full_path())


    def get_filename(self):
        return slugify(self.name)

    def getmd5(self):
        f = self.datei.open()
        md5 = hashlib.md5()
        for chunk in iter(lambda: f.read(128*md5.block_size), ''):
            md5.update(chunk)
        return md5.digset()

    def move_if_path_changed(self,save=True):
        old_path = self.datei.name
        new_path = self.get_full_path()
        if old_path != new_path:
            self._file_move(
                os.path.join(settings.MEDIA_ROOT,old_path),
                os.path.join(settings.MEDIA_ROOT,new_path))
            self.datei.name=new_path
            self.pfad=new_path
            if save: self.save()


    def save(self, *args, **kwargs):
        # wenn datei bereits in db und 
        # pfad unterschiedlich: verschieben
        if self.id:
            self.move_if_path_changed(save=False)
            super(Lernhilfe, self).save()
        else:
            #TODO gibt es eine bessere lösung?
            super(Lernhilfe, self).save()
            self.md5sum=self.getmd5()
            super(Lernhilfe, self).save()


    def delete(self, *args, **kwargs):
        try:
            os.remove(self.datei.path)
        except os.error:
            pass
        super(Lernhilfe, self).delete()


    def _create_folder_if_not_exists(self):
        d = os.path.dirname(self.get_full_abs_path())
        if not os.path.exists(d):
            os.makedirs(d)

    def _file_move(self, old, new):
        self._create_folder_if_not_exists()
        if os.path.exists(new): raise ValidationError('Datei bereits vorhanden')
        os.rename(old,new)

    def __unicode__(self):
        return self.name


class Dozent(AbstractHasPath):
    class Meta:
        verbose_name="Dozent"
        verbose_name_plural="Dozenten"
    nachname = models.CharField('Nachname',max_length=200)
    vorname  = models.CharField('Vorname',max_length=200)

    def __unicode__(self):
        return self.nachname+ ', ' +self.vorname


class Semester(AbstractHasPath):
    class Meta:
        verbose_name="Semester"
        verbose_name_plural="Semester"
    HAELFTE_CHOISES=(
        ('ss','SS'),
        ('ws','WS')
    )
    jahr = models.IntegerField('Jahr')
    haelfte = models.CharField('Hälfte',max_length=2,choices=HAELFTE_CHOISES)
    def __unicode__(self):
        return str(self.jahr)+ '-' +self.haelfte


