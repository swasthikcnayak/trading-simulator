import imp
from django.contrib import admin
from django.urls import path, include
from user.views import profile

urlpatterns = [
    path('profile/', profile ,name='profile')
]
