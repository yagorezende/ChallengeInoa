from django.urls import path

from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login', system_login, name='login'),
    path('logout', system_logout, name='logout'),
]
