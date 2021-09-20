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
import io
import os
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf


class HomeView(TemplateView):
	template_name = 'home.html'


class MonthView(ListView):
    template_name = 'month.html'
    model = Month

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ven'] = Vendor.objects.filter(username=self.request.user)
        context['month'] = Month.objects.all()
        return context

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
		return reverse('proapp:month')




def profile(request, id):
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
        detail.bmonth = Month.objects.get(id=id)
        detail.save()
        return HttpResponseRedirect(request.path_info)
      

    else:
        bdata=Details.objects.filter(author_id=request.user.id, bmonth_id=id)
        totalsells = sum(bdata.values_list('totalsell', flat=True))
        totalsthaniyakar = sum(bdata.values_list('sthaniyakar', flat=True))
        totalprice = sum(bdata.values_list('price', flat=True))
        totalsewaprice = sum(bdata.values_list('sewaprice', flat=True))

        return render(request,"detailcreate.html", {'bdatas':bdata, 'tsell':str(totalsells), 'tsthaniyakar':str(totalsthaniyakar), 'tprice':str(totalprice), 'tsewaprice':str(totalsewaprice)})





def kharid(request, id):
    if request.method == 'POST':
        month_id = request.GET.get('month_id')
        khariddate = request.POST.get('khariddate')
        kharidbijan = request.POST.get('kharidbijan')
        aapurtiname = request.POST.get('aapurtiname')
        aapurtilekha = request.POST.get('aapurtilekha')
        pauthariname = request.POST.get('pauthariname')
        pauthariquantity =request.POST.get('pauthariquantity')
        totalbuyprice = request.POST.get('totalbuyprice')
        pautharitotalprice = request.POST.get('pautharitotalprice')
        buyprice = request.POST.get('buyprice')
        tax = request.POST.get('tax')
        taxbuyprice = (int(buyprice)*int(tax))/100
        pauthariprice = request.POST.get('pauthariprice')
        pautharitax = request.POST.get('pautharitax')
        pautharitaxprice = (int(pauthariprice)*int(pautharitax))/100
        pujigatprice = request.POST.get('pujigatprice')
        pujigattax = request.POST.get('pujigattax')
        pujigattaxprice = (int(pujigatprice)*int(pujigattax))/100
        # detail.instance.author = request.user
        
        detail = Khariddata(khariddate=khariddate, kharidbijan=kharidbijan, aapurtiname=aapurtiname, aapurtilekha=aapurtilekha, pauthariname=pauthariname, pauthariquantity=pauthariquantity, totalbuyprice=totalbuyprice, pautharitotalprice=pautharitotalprice, buyprice=buyprice, tax=tax, taxbuyprice=taxbuyprice, pauthariprice=pauthariprice, pautharitax=pautharitax, pautharitaxprice=pautharitaxprice, pujigatprice=pujigatprice, pujigattax=pujigattax, pujigattaxprice=pujigattaxprice, owner=request.user)
        detail.kmonth = Month.objects.get(id=id)
        detail.save()
        return HttpResponseRedirect(request.path_info)
      

    else:
        vendor = Vendor.objects.filter(username=request.user)
        data = Khariddata.objects.filter(owner_id=request.user.id, kmonth_id=id)
        totalsells = sum(data.values_list('totalbuyprice', flat=True))
        totalsthaniyakar = sum(data.values_list('pautharitotalprice', flat=True))
        totalprice = sum(data.values_list('buyprice', flat=True))
        taxbuyprice = sum(data.values_list('taxbuyprice', flat=True))
        pauthariprice = sum(data.values_list('pauthariprice', flat=True))
        pautharitaxprice = sum(data.values_list('pautharitaxprice', flat=True))
        pujigatprice = sum(data.values_list('pujigatprice', flat=True))
        pujigattaxprice = sum(data.values_list('pujigattaxprice', flat=True))


        return render(request,"baisakh.html", {'datas':data, 'ven':vendor, 'tsell':str(totalsells), 'tsthaniyakar':str(totalsthaniyakar), 'tprice':str(totalprice), 'tsewaprice':str(taxbuyprice), 'tpauthariprice':str(pauthariprice), 'tpautharitaxprice':str(pautharitaxprice), 'tpujigat':str(pujigatprice), 'tpujigattaxprice':str(pujigattaxprice)})




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
        student.sewaprice = sewaprice


    if type == "tax":
        student.tax = value
        tax = student.tax
        price = student.price
        sewaprice = (int(price)*int(tax))/100
        student.sewaprice = sewaprice


    if type == "country":
        student.country = value


    if type == "nikasipatra":
        student.nikasipatra = value


    if type == "nikasidate":
        student.nikasidate = value

    student.save()
    return JsonResponse({"success":"Updated"})




def updated(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    student=Khariddata.objects.get(id=id)

    if type=="khariddate":
    	student.khariddate=value

    if type == "kharidbijan":
    	student.kharidbijan = value

    if type == "aapurtiname":
    	student.aapurtiname = value

    if type == "aapurtilekha":
        student.aapurtilekha = value

    if type == "pauthariname":
        student.pauthariname = value

    if type == "pauthariquantity":
        student.pauthariquantity = value

    if type == "totalbuyprice":
        student.totalbuyprice = value

    if type == "pautharitotalprice":
        student.pautharitotalprice = value

    if type == "buyprice":
        student.buyprice = value
        buyprice = student.buyprice
        tax = student.tax
        taxbuyprice = (int(buyprice)*int(tax))/100
        student.taxbuyprice = taxbuyprice


    if type == "tax":
        student.tax = value
        tax = student.tax
        buyprice = student.buyprice
        taxbuyprice = (int(buyprice)*int(tax))/100
        student.taxbuyprice = taxbuyprice

    if type == "pauthariprice":
        student.pauthariprice = value
        pauthariprice = student.pauthariprice
        pautharitax = student.pautharitax
        pautharitaxprice = (int(pauthariprice)*int(pautharitax))/100
        student.pautharitaxprice = pautharitaxprice


    if type == "pautharitax":
        student.pautharitax = value
        pautharitax = student.pautharitax
        pauthariprice = student.pauthariprice
        pautharitaxprice = (int(pauthariprice)*int(pautharitax))/100
        student.pautharitaxprice = pautharitaxprice


    if type == "pujigatprice":
        student.pujigatprice = value
        pujigatprice = student.pujigatprice
        pujigattax = student.pujigattax
        pujigattaxprice = (int(pujigatprice)*int(pujigattax))/100
        student.pujigattaxprice = pujigattaxprice


    if type == "pujigattax":
        student.pujigattax = value
        pujigattax = student.pujigattax
        pujigatprice = student.pujigatprice
        pujigattaxprice = (int(pujigatprice)*int(pujigattax))/100
        student.pujigattaxprice = pujigattaxprice


    student.save()
    return JsonResponse({"success":"Updated"})

	

	

class ProfileView(TemplateView):
	template_name = "profile.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) 
		posts = Vendor.objects.all()
		context['posts'] = posts
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
		return redirect('proapp:month')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('proapp:month')
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
		return render(request, 'baisakh.html')



def delete(request, id):
	if request.method=="POST":
		pi = Khariddata.objects.filter(id=id)
		pi.delete()
		return render(request, 'detailcreate.html')


def save_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=record.csv'
	writer = csv.writer(response)
	record = Details.objects.filter(author=request.user)
	infoma = Vendor.objects.filter(username=request.user)
	writer.writerow(['','','','','','','Bikri Khata'])
	for inf in infoma:
		writer.writerow(['', '', 'Pan: ', inf.pan,'Kardarta Name: ',inf.kardartaname,'Year: ',inf.year,'Duration: ',inf.duration])

	writer.writerow(['','','','Bijak','','','','|Karyogya Bikri','','|Nikasi','','',''])
	writer.writerow(['dateof','bijan','kharidname','kharidlekha','sewaname','totalsell','sthaniyakar','price','tax','sewaprice','country','nikasipatra','nikasidate'])
	for rec in record:
		writer.writerow([rec.dateof, rec.bijan, rec.kharidname, rec.kharidlekha, rec.sewaname, rec.totalsell, rec.sthaniyakar, rec.price, rec.tax, rec.sewaprice, rec.country, rec.nikasipatra, rec.nikasidate])

	return response




class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
     	context = Khariddata.objects.filter(owner=request.user)
     	vendor = Vendor.objects.filter(username=request.user)
     	totalsells = sum(context.values_list('totalbuyprice', flat=True))
     	totalsthaniyakar = sum(context.values_list('pautharitotalprice', flat=True))
     	totalprice = sum(context.values_list('buyprice', flat=True))
     	taxbuyprice = sum(context.values_list('taxbuyprice', flat=True))
     	pauthariprice = sum(context.values_list('pauthariprice', flat=True))
     	pautharitaxprice = sum(context.values_list('pautharitaxprice', flat=True))
     	pujigatprice = sum(context.values_list('pujigatprice', flat=True))
     	pujigattaxprice = sum(context.values_list('pujigattaxprice', flat=True))
     	pdf = render_to_pdf('pdf_template.html', {'context': context, 'ven':vendor, 'tsell':str(totalsells), 'tsthaniyakar':str(totalsthaniyakar), 'tprice':str(totalprice), 'tsewaprice':str(taxbuyprice), 'tpauthariprice':str(pauthariprice), 'tpautharitaxprice':str(pautharitaxprice), 'tpujigat':str(pujigatprice), 'tpujigattaxprice':str(pujigattaxprice)})
     	return HttpResponse(pdf, content_type='application/pdf')



# Create your views here.
