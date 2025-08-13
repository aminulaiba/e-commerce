from django.urls import path
from . import views
appname = 'cart'
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/', views.cart_add, name='add'),
    path('delete/', views.cart_delete, name='cart-delete'),
    path('update/', views.cart_update, name='cart-update'),
    
] 