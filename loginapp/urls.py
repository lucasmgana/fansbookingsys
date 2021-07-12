from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

from . import payment
from .tickect import *

app_name = '<loginapp>'

urlpatterns = [

    path('register/', register, name='register'),
    path('', HomeView.as_view(), name='home'),
    path('ticket/<int:pk>/', TicketView.as_view(), name = 'ticket'),
    path('tickets/<int:pk>/', ListTicketView.as_view(), name = 'tickets'),

    path('payment/<int:pk>/', payment.payment, name = 'payment'),
    path('/<int:pk>/', payment.repay, name = 'repay'),
    path('successfully/', SuccessfullyView.as_view(), name = 'successfully'),

    # path('', index),
    path('ticket_view/<int:pk><str:tn>/', ViewTicket.as_view(), name="ticket_view"),
    path('ticket_download/<int:pk><str:tn>/', DownloadTicket.as_view(), name="ticket_download"),

    ] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)


