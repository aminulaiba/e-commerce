from django.urls import path
from . import views

appname = 'payments'

urlpatterns = [
    path('', views.order_details, name='checkout'),
    
] 