from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

from . import payment

app_name = '<loginapp>'

urlpatterns = [

    path('register/', register, name='register'),
    path('', HomeView.as_view(), name='home'),
    path('ticket/<int:pk>/', TicketView.as_view(), name = 'ticket'),
    path('tickets/<int:pk>/', ListTicketView.as_view(), name = 'tickets'),
    path('payment/<int:pk>/', payment.payment, name = 'payment'),
    path('successfully/', SuccessfullyView.as_view(), name = 'successfully'),

    ] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)


