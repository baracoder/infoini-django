from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class News(models.Model):
	title = models.CharField('Titel',max_length=100)
	text  = models.TextField()
	pub_date = models.DateField(auto_now_add=True)
	author = models.ForeignKey(User)
	category = models.ForeignKey('Category')

	def __unicode__(self):
		return self.title


class Category(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

admin.site.register(News)
admin.site.register(Category)
