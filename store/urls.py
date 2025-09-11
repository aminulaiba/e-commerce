from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('update-user/', views.update_user, name='update-user'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('pass-change/', views.password_change, name='password-change'),
    path('detail/<int:pk>', views.product, name='product'),
    path('category/<str:name>', views.category, name='category'),
] 