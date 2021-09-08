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
	path('blog/create',VendorCreateView.as_view(),name='blogcreate'),
	path('changepass/', views.changepPass, name='changepass'),
	# path('detailcreate/', DetailCreateView.as_view(), name='detailcreate'),
	path('detailcreate/', views.profile, name='detailcreate'),
	path('update/', views.update, name='update'),
	path('showdata/', views.show_all_data, name='showdata'),
	path('remove/<int:id>/', views.remove, name='remove'),
]