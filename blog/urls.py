from django.contrib import admin
from django.urls import path
from .views import create_post, index, about, login, recents, relevants, signin, logout, view_post

urlpatterns = [
    path('', index, name="index"),
    path('about', about, name="about"),
    path('login', login, name="login"),
    path('signin', signin, name="signin"),
    path('logout', logout, name="logout"),
    path('recents', recents, name="recents"),
    path('relevants', relevants, name="relevants"),
    path('create_post', create_post, name="create_post"),
    path('post/<uuid:id>', view_post, name="view_post"),
]
