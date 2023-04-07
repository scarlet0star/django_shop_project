from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path("", product_list, name='products'),
    path("create/", product_create, name='product_create'),
    path("inbound/", inbound_list, name='inbounds'),
    path("inbound/create", inbound_create, name='inbound_create'),
    path("outbound/", outbound_list, name='outbounds'),
    path("outbound/create", outbound_create, name='outbound_create'),
    path("inventory/", inventory, name='inventory'),
]
