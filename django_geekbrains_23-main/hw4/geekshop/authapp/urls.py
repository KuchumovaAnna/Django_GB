from django.urls import include, re_path
from authapp import views

app_name ='authapp'

urlpatterns = [
	re_path(r'^$', views.login),
	re_path(r'^login/$', views.login, name='login'),
	re_path(r'^logout/$', views.logout, name='logout'),
	re_path(r'^registration/$', views.registration, name='registration'),
	re_path(r'^restore/$', views.restore, name='restore'),
]


