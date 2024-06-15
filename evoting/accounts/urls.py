from django.urls import path
from .views import *

urlpatterns = [
    path('login-admin/', admin_login, name='admin_login'),
    path('logout-admin/', admin_logout, name='admin_logout'),
    path('register-admin/', admin_register, name='admin_register'),
    path('pemilih-login/', pemilih_login, name='pemilih_login'),
    path('pemilih-logout/', pemilih_logout, name='pemilih_logout'),
]
