from django.shortcuts import reverse ,redirect
from django.views.generic import * #TemplateView,ListView,DetailView,CreateView,UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
import csv

class HomeView(TemplateView):
	template_name = 'home.html'




class VendorCreateView(LoginRequiredMixin, CreateView):
	template_name = "signupform.html"
	model = Vendor
	form_class = VendorCreateForm

	def form_valid(self, form):
		# messages.success(self.request, 'form is valid')
		if self.request.method == "POST":
			form.instance.username = self.request.user
			form.instance.user_id = self.request.user.id
			u_add=form.cleaned_data['address']
			pan = form.cleaned_data['pan']
			kardartaname = form.cleaned_data['kardartaname']
			year = form.cleaned_data['year']
			duration = form.cleaned_data['duration']
		
			form.save()
		return redirect(self.get_success_url())

	def get_success_url(self):
		return reverse('proapp:detailcreate')




def profile(request):
    if request.method == 'POST':
        dateof = request.POST.get('dateof')
        bijan = request.POST.get('bijan')
        kharidname = request.POST.get('kharidname')
        kharidlekha = request.POST.get('kharidlekha')
        sewaname = request.POST.get('sewaname')
        totalsell =request.POST.get('totalsell')
        sthaniyakar = request.POST.get('sthaniyakar')
        price = request.POST.get('price')
        tax = request.POST.get('tax')
        sewaprice = (int(price)*int(tax))/100
        country = request.POST.get('country')
        nikasipatra = request.POST.get('nikasipatra')
        nikasidate = request.POST.get('nikasidate')
        # detail.instance.author = request.user
        
        detail = Details(
                    dateof=dateof, bijan=bijan, kharidname=kharidname, kharidlekha=kharidlekha, sewaname=sewaname, totalsell=totalsell, sthaniyakar=sthaniyakar, price=price, tax=tax, sewaprice=sewaprice, country=country, nikasipatra=nikasipatra, nikasidate=nikasidate, author=request.user)
        detail.save()
        return HttpResponseRedirect('/detailcreate/')
      

    else:
    	student=Details.objects.filter(author=request.user)
    	vendor = Vendor.objects.filter(username=request.user)
    	totalsells = sum(student.values_list('totalsell', flat=True))
    	totalsthaniyakar = sum(student.values_list('sthaniyakar', flat=True))
    	totalprice = sum(student.values_list('price', flat=True))
    	totalsewaprice = sum(student.values_list('sewaprice', flat=True))

    	return render(request,"detailcreate.html", {'students':student, 'ven':vendor, 'tsell':str(totalsells), 'tsthaniyakar':str(totalsthaniyakar), 'tprice':str(totalprice), 'tsewaprice':str(totalsewaprice)})




def show_all_data(request):
    student=Details.objects.filter(author=request.user)
    vendor = Vendor.objects.filter(username=request.user)
    totalsells = sum(student.values_list('totalsell', flat=True))
    totalsthaniyakar = sum(student.values_list('sthaniyakar', flat=True))
    totalprice = sum(student.values_list('price', flat=True))
    totalsewaprice = sum(student.values_list('sewaprice', flat=True))

    return render(request,"showdata.html", {'students':student, 'ven':vendor, 'tsell':str(totalsells), 'tsthaniyakar':str(totalsthaniyakar), 'tprice':str(totalprice), 'tsewaprice':str(totalsewaprice)})


def update(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    student=Details.objects.get(id=id)

    if type=="dateof":
       student.dateof=value

    if type == "bijan":
        student.bijan = value

    if type == "kharidname":
        student.kharidname = value

    if type == "kharidlekha":
        student.kharidlekha = value

    if type == "sewaname":
        student.sewaname = value

    if type == "totalsell":
        student.totalsell = value

    if type == "sthaniyakar":
        student.sthaniyakar = value

    if type == "price":
        student.price = value
        price = student.price
        tax = student.tax
        sewaprice = (int(price)*int(tax))/100
        print(sewaprice)
        student.sewaprice = sewaprice


    if type == "tax":
        student.tax = value
        tax = student.tax
        price = student.price
        sewaprice = (int(price)*int(tax))/100
        print(sewaprice)
        student.sewaprice = sewaprice


    if type == "country":
        student.country = value


    if type == "nikasipatra":
        student.nikasipatra = value


    if type == "nikasidate":
        student.nikasidate = value

    student.save()
    return JsonResponse({"success":"Updated"})

	

class ProfileView(TemplateView):
	template_name = "profile.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) 
		posts = Vendor.objects.all()
		context['posts'] = posts
		print(posts)
		return context

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('proapp:home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('proapp:login')
			

		context = {'form':form}
		return render(request, 'register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('proapp:detailcreate')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('proapp:detailcreate')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('proapp:login')




class BlogCreateForm(CreateView):
	template_name = "blogcreate.html"
	model = Details
	form_class = VendorCreateForm

	def form_valid(self, form):
		# messages.success(self.request, 'form is valid')
		form.instance.author = self.request.user
		form.save()
		return redirect(self.get_success_url())

	def get_success_url(self):
		return reverse('proapp:home')




def changepPass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            v = form.save()
            update_session_auth_hash(request, v)
            messages.success(request, 'Password Changed!!')
            return redirect('proapp:home')
    else:
        form = PasswordChangeForm(request.user)
    params = {
        'form':form,
    }
    return render(request, 'changepass.html', params)


def remove(request, id):
	if request.method=="POST":
		pi = Details.objects.filter(id=id)
		pi.delete()
		return HttpResponseRedirect('/detailcreate/')


def save_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=record.csv'
	writer = csv.writer(response)
	record = Details.objects.filter(author=request.user)
	writer.writerow(['dateof','bijan','kharidname','kharidlekha','sewaname','totalsell','sthaniyakar','price','tax','sewaprice','country','nikasipatra','nikasidate'])
	for rec in record:
		writer.writerow([rec.dateof, rec.bijan, rec.kharidname, rec.kharidlekha, rec.sewaname, rec.totalsell, rec.sthaniyakar, rec.price, rec.tax, rec.sewaprice, rec.country, rec.nikasipatra, rec.nikasidate])

	return response
# Create your views here.
