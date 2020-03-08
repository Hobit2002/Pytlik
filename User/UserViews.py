from django.shortcuts import render, redirect
from django.template import RequestContext
import json, re,time,sys,os, time
from pathlib import Path
from django.urls import path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Authentication, Database, LanguageLoader
# Create your views here.

def Home(request):
    LanguagePack = LanguageLoader.Language("HomePage","Czech")
    Decision  = Authentication.CheckUser(request,"User\HomePage.html",LanguagePack)  
    return Decision

def Settings(request):
    LanguagePack = LanguageLoader.Language("Settings","Czech")
    Decision  = Authentication.CheckUser(request,"User\Settings.html",LanguagePack)
    return Decision

def Saving(request):
    Authentication.QuickCheck(request)
    FirstName = request.POST["FirstName"]
    SecondName = request.POST["SecondName"]
    Email =  request.POST["Email"]
    Year = request.POST["Year"]
    Info = request.POST["Info"]
    Sex = request.POST["Sex"]
    ID = Authentication.GetID(request)
    Database.UpdateUser(FirstName, SecondName, Email, Year, Info, ID)
    response = redirect ('Home')
    response.delete_cookie('MetaInfo')
    return response