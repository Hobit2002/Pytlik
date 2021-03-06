"""Pytlik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from registrationstuff import RegistrationViews
from User import UserViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Niemand.urlsNiemand')),
    path('login',include('registrationstuff.urlsRegistrationstuff')),
    path('registration',RegistrationViews.registration, name="Registration"),
    path('FinishReg',RegistrationViews.USRvertify,name="USRvertify"),
    path('PutMeIn',RegistrationViews.SendMail, name="SendMail"),
    path('PutOut',RegistrationViews.Putout, name="Putout"),
    path('Home',UserViews.Home, name ="Home"),
    path('settings',UserViews.Settings, name ="Settings"),
    path('SetProfile',UserViews.Saving, name ="Saving"),
    path('MyPasive',UserViews.Pasives, name ="PassiveUsers"),
    path('NewPassives',UserViews.NewPasives, name ="NewPassiveUsers"),
    path('FindAndKill',UserViews.FindAndKill, name ="FindAndKill"),
    path('NewProduct',UserViews.NewProduct, name ="NewProduct"),
    path('Product',UserViews.Product, name ="Product"),
    path('NewProductHero',UserViews.NewProductHero, name ="NewProductHero"),
    path('DeleteHero',UserViews.DeleteHero, name ="DeleteHero"),
    path('DeleteTask',UserViews.DeleteTask, name ="DeleteTask"),
    path('NewTask',UserViews.NewTask, name ="NewTask"),
    path('SelfDeleteHero',UserViews.SelfDeleteHero, name ="SelfDeleteHero"),
    path('DeleteProduct',UserViews.DeleteProduct, name ="DeleteProduct"),
    path('NewTaskHero',UserViews.NewTaskHero, name ="NewTaskHero"),
    path('DeleteTaskHero',UserViews.DeleteTaskHero, name ="DeleteTaskHero"),
    path('ResetTaskTime',UserViews.ResetTaskTime, name ="ResetTaskTime"),
    path('Search',UserViews.Search, name="Search"),
    path('Diary',UserViews.Diary, name="Diary"),
    path('SubmitDiary',UserViews.SubmitDiary, name="SubmitDiary"),
    path('HeroSelfInclude',UserViews.HeroSelfInclude, name="HeroSelfInclude"),
    path('Calendar',UserViews.Calendar, name="Calendar"),
    path('CallDay',UserViews.CallDay, name="CallDay"),
    path('NewProject',UserViews.NewProject, name="NewProject"),
    path('Project',UserViews.Project, name="Project"),
    path('NewProjectHero',UserViews.NewProjectHero, name ="NewProjectHero"),
    path('DeleteProject',UserViews.DeleteProject, name ="DeleteProject"),
    path('DeleteProjectHero',UserViews.DeleteProjectHero, name ="DeleteProjectHero"),
    path('NewProjectProduct',UserViews.NewProjectProduct, name ="NewProjectProduct"),
    path('NewComment',UserViews.NewComment, name="NewComment"),
    path('AnswerProductComment',UserViews.AnswerProductComment, name="AnswerProductComment"),
    path('DeleteNotification',UserViews.DeleteNotification, name="DeleteNotification"),
    path('MarkNotificationAsRead',UserViews.MarkNotificationAsRead, name="MarkNotificationAsRead"),
    path('SendChat',UserViews.SendChat, name="SendChat"),
    path('UpdateConversation',UserViews.UpdateConversation, name="UpdateConversation"),
    path('MarkReaded',UserViews.MarkReaded, name="MarkReaded")
    ]
urlpatterns += staticfiles_urlpatterns()