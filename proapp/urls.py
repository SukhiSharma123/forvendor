from django.urls import path
from .views import * 
from django.contrib.sitemaps.views import sitemap
from . import views

app_name = 'proapp'
urlpatterns =[
	path('',HomeView.as_view(),name='home'),
	# path('details/',SignupFormView.as_view(),name="details"),
	# path('profile/', views.profile, name='profile'),
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
	path('profile/', ProfileView.as_view(), name="profile"),
	path('month/', MonthView.as_view(), name="month"),
	path('blog/create',VendorCreateView.as_view(),name='blogcreate'),
	path('changepass/', views.changepPass, name='changepass'),
	# path('detailcreate/', DetailCreateView.as_view(), name='detailcreate'),
	path('detailcreate/<int:id>', views.profile, name='detailcreate'),
	path('kharidcreate/<int:id>/', views.kharid, name='kharidcreate'),
	path('update/', views.update, name='update'),
	path('updated/', views.updated, name='updated'),
	path('remove/<int:id>/', views.remove, name='remove'),
	path('delete/<int:id>/', views.delete, name='delete'),
	path('savecsv/', views.save_csv, name='savecsv'),
	path('savepdf/<int:pk>/', GeneratePdf.as_view(), name='savepdf'),
]