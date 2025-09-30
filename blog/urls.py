from django.contrib import admin
from django.urls import path
from .views import index, about, login, logout, signin, protected_route

urlpatterns = [
    path('', index, name="index"),
    path('about', about, name="about"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('signin', signin, name="signin"),
    path('protected', protected_route, name="protected"),
]
