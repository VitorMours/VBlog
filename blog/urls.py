from django.contrib import admin
from django.urls import path
from .views import index, about, login, signin, dashboard

urlpatterns = [
    path('', index, name="index"),
    path('about', about, name="about"),
    path('login', login, name="login"),
    path('signin', signin, name="signin"),
    path('dashboard', dashboard, name="dashboard"),
]
