
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import RegistrationViews

urlpatterns = [
    path('',RegistrationViews.login, name="login"),
    ]
urlpatterns += staticfiles_urlpatterns()
