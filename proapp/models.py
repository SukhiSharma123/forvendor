from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Vendor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	username = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	pan = models.CharField(max_length=30)
	kardartaname = models.CharField(max_length=200)
	year = models.CharField(max_length=6)
	duration = models.CharField(max_length=10)


	def __str__(self):
		return str(self.user.id)



class Details(models.Model):
	dateof = models.CharField(max_length=20, unique=True)
	bijan = models.CharField(max_length=30)
	kharidname = models.CharField(max_length=200)
	kharidlekha = models.CharField(max_length=30)
	sewaname = models.CharField(max_length=200)
	totalsell = models.IntegerField()
	sthaniyakar = models.IntegerField()
	price = models.IntegerField()
	tax = models.IntegerField()
	sewaprice = models.IntegerField()
	country = models.CharField(max_length=30)
	nikasipatra = models.CharField(max_length=30)
	nikasidate = models.CharField(max_length=20)
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="post")

	def __unicode__(self):
		return str(self.id)
