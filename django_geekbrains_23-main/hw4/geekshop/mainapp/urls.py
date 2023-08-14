from django.urls import include, re_path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
	re_path(r'^(?P<dir1>\d+)-(?P<dir2>\d+)/(?P<vend>\w+)$', views.item, name='item'),
	re_path(r'^(?P<dir1>\d+)-(?P<dir2>\d+)/*$', views.catalog, name='items'),
	re_path(r'^$', views.catalog, name='catalog'),

]


