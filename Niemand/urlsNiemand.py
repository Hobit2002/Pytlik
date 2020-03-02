from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.gate, name="gate"),
   ]
urlpatterns += staticfiles_urlpatterns()
