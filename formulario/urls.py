
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',  views.INCRUSTADO, name='INCRUSTADO'),
    path('paid/', views.PAID, name='PAID'),
    path('ipn/', views.IPN, name='IPN')
]
