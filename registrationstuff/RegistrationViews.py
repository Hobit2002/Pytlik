from django.shortcuts import render
from django.template import RequestContext
import json, re,time,sys,os, time
from pathlib import Path
from django.urls import path
from django.shortcuts import redirect
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Authentication, Database


#1.
def login(request):
     #1.1.2. - b) Get content of page
     ReadIt = Path('languages\Pages.txt')
     InnerText = ReadIt.read_text()
     Pages =json.loads(InnerText)
     PageContent = Pages["Login"]
     #1.1.3. -b) And translate it into language of page
     #1.1.3.1 -b)Load dictionary
     ReadIt = Path('languages\Dictionary.txt')
     InnerText = ReadIt.read_text()
     Dictionary =json.loads(InnerText)
     #1.1.3.2 - b)Choose right language
     Language = "Czech"
     Language = Dictionary[Language]
     #1.1.3.3. -b) Finally translate
     LanguagePack = {}
     for ToTranslate in PageContent:
         LanguagePack[ToTranslate] = Language[ToTranslate]

     return render(request, "Registrationstuff\Login.html",LanguagePack)

#2.
def registration(request):
     #1.1. - b) If you can´t recognize any user, direct visitor on home page
     #1.1.2. - b) Get content of page
     ReadIt = Path('languages\Pages.txt')
     InnerText = ReadIt.read_text()
     Pages =json.loads(InnerText)
     PageContent = Pages["Registration"]
     #1.1.3. -b) And translate it into language of page
     #1.1.3.1 -b)Load dictionary
     ReadIt = Path('languages\Dictionary.txt')
     InnerText = ReadIt.read_text()
     Dictionary =json.loads(InnerText)
     #1.1.3.2 - b)Choose right language
     Language = "Czech"
     Language = Dictionary[Language]
     #1.1.3.3. -b) Finally translate
     LanguagePack = {}
     for ToTranslate in PageContent:
         LanguagePack[ToTranslate] = Language[ToTranslate]

     return render(request, "Registrationstuff\Registration.html", LanguagePack)

 #3. Registrate new users
def Putin(request):
    FirstName = request.POST["FirstName"]
    SecondName = request.POST["SecondName"]
    Email =  request.POST["Email"]
    Birthdate = request.POST["Birthdate"]
    Password1 = request.POST["password1"]
    Password2 = request.POST["password2"]
    if Password1==Password2:
        ID = Database.DP2(FirstName,SecondName,Password1,Email,"",Birthdate)
        token = Authentication.Authenticate(request,ID)
    else:
        return render(request, "User\HomePage.html")

         #1.1. - b) If you can´t recognize any user, direct visitor on home page
     #1.1.2. - b) Get content of page
    ReadIt = Path('languages\Pages.txt')
    InnerText = ReadIt.read_text()
    Pages =json.loads(InnerText)
    PageContent = Pages["HomePage"]
    #1.1.3. -b) And translate it into language of page
    #1.1.3.1 -b)Load dictionary
    ReadIt = Path('languages\Dictionary.txt')
    InnerText = ReadIt.read_text()
    Dictionary =json.loads(InnerText)
    #1.1.3.2 - b)Choose right language
    Language = "Czech"
    Language = Dictionary[Language]
    #1.1.3.3. -b) Finally translate
    LanguagePack = {}
    for ToTranslate in PageContent:
        LanguagePack[ToTranslate] = Language[ToTranslate]

    LanguagePack["FirstName"] = FirstName
    LanguagePack["OtherNames"] = SecondName
    LanguagePack["token"] = token
    return render(request, "User\HomePage.html", LanguagePack)
     
 #3. Login already registred
def Putout(request):
    Email =  request.POST["email"]
    Password = request.POST["password"]
    try:
        ID, FirstName, OtherNames, Image, Info, Sex, Birthday, Year = Database.DP3(Password,Email)
        token = Authentication.Authenticate(request,ID)
        #1.1. - b) If you can´t recognize any user, direct visitor on home page
        #1.1.2. - b) Get content of page
        ReadIt = Path('languages\Pages.txt')
        InnerText = ReadIt.read_text()
        Pages =json.loads(InnerText)
        PageContent = Pages["HomePage"]
                #1.1.3. -b) And translate it into language of page
        #1.1.3.1 -b)Load dictionary
        ReadIt = Path('languages\Dictionary.txt')
        InnerText = ReadIt.read_text()
        Dictionary =json.loads(InnerText)
        #1.1.3.2 - b)Choose right language
        Language = "Czech"
        Language = Dictionary[Language]
        #1.1.3.3. -b) Finally translate
        LanguagePack = {}
        for ToTranslate in PageContent:
            LanguagePack[ToTranslate] = Language[ToTranslate]

        LanguagePack["FirstName"] = FirstName
        LanguagePack["OtherNames"] = OtherNames        
        LanguagePack["token"] = token
        return render(request, "User\HomePage.html", LanguagePack)

    except:
        return redirect('login')

         