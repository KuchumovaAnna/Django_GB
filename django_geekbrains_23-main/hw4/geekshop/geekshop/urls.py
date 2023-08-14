from django.contrib import admin
from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static
from mainapp import views, urls

urlpatterns = [
	re_path(r'^$', views.main, name = 'main'),
	re_path('^delivery/', views.delivery, name = 'delivery'),
	re_path('^help/', views.help, name = 'help'),
	re_path('^admin/', admin.site.urls),
	re_path('^catalog/', include('mainapp.urls',namespace = 'catalog')),
	re_path('^auth/', include('authapp.urls', namespace ='auth')),
	re_path('^basket/', include('basketapp.urls', namespace ='basket')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)