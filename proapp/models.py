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


class Khariddata(models.Model):
	khariddate = models.CharField(max_length=20)
	kharidbijan = models.CharField(max_length=20)
	aapurtiname = models.CharField(max_length=200)
	aapurtilekha = models.CharField(max_length=20)
	pauthariname = models.CharField(max_length=200)
	pauthariquantity = models.IntegerField()
	totalbuyprice = models.IntegerField()
	pautharitotalprice = models.IntegerField()
	buyprice = models.IntegerField()
	tax = models.IntegerField()
	taxbuyprice = models.IntegerField()
	pauthariprice = models.IntegerField()
	pautharitax = models.IntegerField()
	pautharitaxprice = models.IntegerField()
	pujigatprice = models.IntegerField()
	pujigattax = models.IntegerField()
	pujigattaxprice = models.IntegerField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="posts")


	def __unicode__(self):
		return str(self.id)
