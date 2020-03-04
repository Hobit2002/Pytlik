from django.shortcuts import render,redirect
from django.template import RequestContext
import json, re,time,sys,os
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Authentication,LanguageLoader

#1.
def gate(request):
    #1.1.Direct user on appropriate page
    try:
        #1.1. -a) If user is logged in, direct him on his profile.
        Wish = redirect("Home")
        Decision  = Authentication.CheckUser(request,Wish)  
        return Decision

    
    except:
        #1.1. - b) If you can´t recognize any user, direct visitor on home page
        #1.1.2. - b) Get content of page
        LanguagePack = LanguageLoader.Language("AboutUs","Czech")
        return render(request,"Niemand\AboutUs.html", LanguagePack)


