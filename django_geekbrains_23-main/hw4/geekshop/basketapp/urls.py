from django.urls import include, re_path
from basketapp import views

app_name ='basketapp'

urlpatterns = [
	re_path(r'^$', views.basket, name='basket'),
	re_path(r'^add/$', views.add_item, name='add'),
	re_path(r'^del/(?P<v_code>\w+)$', views.del_item, name='del'),
	re_path(r'^del/$', views.basket, name='del_null'),
	re_path(r'^buy/$', views.buy, name='buy'),
	#re_path(r'^update/$', views.update_row, name='update'),
]
