from django.urls import path
from . import views 

urlpatterns = [
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
	path('upload', views.upload, name='upload'),
	path('register', views.register, name='register'),
	path('uploadrules',views.uploadrules,name = 'uploadrules')
]
