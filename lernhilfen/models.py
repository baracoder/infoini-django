from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
import os

class Typ(models.Model):
    name = models.CharField(max_length=100)
    def get_path(self):
        return slugify(self.name)

class Fach(models.Model):
    name = models.CharField(max_length=100)
    def get_path(self):
        return slugify(self.name)

class Studiengang(models.Model):
    name = models.CharField(max_length=100)
    def get_path(self):
        return slugify(self.name)


class Lernhilfe(models.Model):
    name = models.CharField(max_length=100)
    typ = models.ForeignKey('Typ')
    fach = models.ForeignKey('Fach')
    fachrichtung = models.ForeignKey('Studiengang')
    gesichtet = models.Boolean(default=False)


    def get_filename(self):
        return slugify(self.name)

    def get_full_path(self):
        p = os.path.join(
            settings.LERNHILFEN_ROOT,
            self.fachrichtung.get_path(),
            self.fach.get_path(),
            self.get_filename())
        return os.path.abspath(p)

    def save(self, *args, **kwargs):
        # wenn objekt bereits in db
        if self.id:
            old = self.__class__.objects.get(pk=self._get_pk_val())
            old_path = old.get_full_path()
            new_path = self.get_full_path()
            if old_path != new_path:
                self.file_move(old_path,new_path)

        if not os.path.exits(self.get_full_path()): raise ValidationError('Datei nicht vorhanden')
        super(Lernhilfe, self).save()


    def delete(self, *args, **kwargs):
        self.file_delete()
        super(Lernhilfe, self).delete()


    def _create_folder_if_not_exists(self):
        p = self.get_full_path()
        d = os.path.dirname(p)
        if not os.path.exits(d):
            os.makedirs(d)

    def file_move(self, old, new):
        self._create_folder_if_not_exists()
        if os.path.exits(self.get_full_path()): raise ValidationError('Datei bereits vorhanden')
        os.rename(old,new)


    def file_save(self, f):
        self._create_folder_if_not_exists()
        p = self.get_full_path()
        # TODO
        # datei f speichern


    def file_delete(self):
        p = self.get_full_path()
        os.remove(p)

