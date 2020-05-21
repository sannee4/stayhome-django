from django.contrib import admin
from django.urls import path, include
from .views import register, login_handler, index, profile, about, logout_handler


urlpatterns = [
    path('register/', register),
    path('login/', login_handler),
    path('profile/', profile),
    path('', index),
    path('about/', about),
    path('logout/', logout_handler)
]
