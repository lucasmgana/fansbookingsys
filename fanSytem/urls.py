from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from loginapp import views
static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('loginapp.urls', namespace='loginapp')),
    path("", include('django.contrib.auth.urls')),

]
