from django.contrib import admin
from django.urls import path
from .views import create_post, index, about, login, profile, recents, relevants, signin, logout, view_post, vote_on_post, ai_action

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
    path('profile/', profile, name="profile"),
    path('api/vote/<uuid:post_id>', vote_on_post, name="vote_on_post"),
    path("ai/action/", ai_action, name="ai_action"),

]
