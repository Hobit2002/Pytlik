from django.shortcuts import render,redirect
from django.template import RequestContext
import json, re,time,sys,os, time
from pathlib import Path
from django.urls import path, reverse
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Authentication, Database,LanguageLoader


#1.
def login(request):
     #1.1.2. - b) Get content of page
     LanguagePack = LanguageLoader.Language("Login","Czech")

     return render(request, "Registrationstuff\Login.html",LanguagePack)

#2.
def registration(request):
     #1.1. - b) If you can´t recognize any user, direct visitor on home page
     #1.1.2. - b) Get content of page
     LanguagePack = LanguageLoader.Language("Registration","Czech")

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
        token = Authentication.Authenticate(request,ID,Email)
        ToSend = {"Email":Email,"FirstName":FirstName, "OtherNames":SecondName, "Image":'', "Info":'', "Sex":'', "Birthday":'', "Year":Birthdate, "token":token}
        Response = redirect("Home")
        Response.set_cookie("BasicInfo", json.dumps(ToSend),max_age = 7200)
        return Response
    else:
        return redirect('registration')
    
     
 #3. Login already registred
def Putout(request):
    Email =  request.POST["email"]
    Password = request.POST["password"]
    try:
        ID, FirstName, OtherNames, Image, Info, Sex, Birthday, Year = Database.DP3(Password,Email)
        token = Authentication.Authenticate(request,ID,Email)
        ToSend = {"Email":Email,"FirstName":FirstName, "OtherNames":OtherNames, "Image":Image, "Info":Info, "Sex":Sex, "Birthday":Birthday, "Year":Year, "token":token}
        Response = redirect("Home")
        Response.set_cookie("BasicInfo", json.dumps(ToSend),max_age = 7200)
        return Response
    #1.1. - b) If you can´t recognize any user, redirect visitor on the login page
    except:
        return redirect('loggin')
        