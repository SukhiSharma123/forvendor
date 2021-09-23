from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class VendorCreateForm(forms.ModelForm):
	class Meta:
		model = Vendor
		fields= ['address','pan','kardartaname','year','duration']

class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput())
	password=forms.CharField(widget=forms.PasswordInput())

class DetailCreateForm(forms.ModelForm):
	class Meta:
		model = Details
		fields = ["dateof", "bijan", "kharidname", "kharidlekha", "sewaname", "totalsell", "sthaniyakar", "price", "tax", "sewaprice", "country", "nikasipatra", "nikasidate"]

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class VendorUpdateForm(forms.ModelForm):
	class Meta:
		model = Vendor
		fields= ['address','pan','kardartaname','year','duration']

