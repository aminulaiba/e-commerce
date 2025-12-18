from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_orderpage, name='oms-login'),
    path('logout/', views.logout_orderpage, name='oms-logout'),
    path('dashbord/', views.orders, name='orders'),
    path('api/', views.get_orders, name='orders-api'),
    path('api/dsbcount/', views.quick_dashbord_counts, name='dsb-count'),
    path('api/<int:pk>/', views.get_orders_details, name='order-details'),
] 
