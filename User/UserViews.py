from django.shortcuts import render
from django.template import RequestContext
import json, re,time,sys,os, time
from pathlib import Path
from django.urls import path
from django.shortcuts import redirect
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Authentication, Database, LanguageLoader
# Create your views here.

def Home(request):
    LanguagePack = LanguageLoader.Language("HomePage","Czech")
    Wish = render(request, "User\HomePage.html", LanguagePack)
    Decision  = Authentication.CheckUser(request,Wish)  
    return Decision