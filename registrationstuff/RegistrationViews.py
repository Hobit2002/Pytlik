from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
import json, re,time,sys,os, time, ezgmail, random, threading, math
from pathlib import Path
from django.urls import path, reverse
from urllib.parse import urlencode
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Authentication, Database,LanguageLoader, Consolewriter

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
def Putin(FirstName, OtherNames, Password, Birthdate,Email, request):
    ID = Database.DP2(FirstName,OtherNames,Password,Email,"",Birthdate)
    token = Authentication.Authenticate(request,ID)
    Response = redirect('Home')
    Response.set_cookie("BasicInfo", str(token), max_age = 60*60*24*60)
    return Response
     
 #3. Login already registred
def Putout(request):
    Email =  request.POST["email"]
    Password = request.POST["password"]
    try:
        ID = (Database.DP3(Password,Email))[0]
        token = Authentication.Authenticate(request,ID)
        Response = redirect('Home')
        Response.set_cookie("BasicInfo", str(token), max_age = 60*60*24*60)
        return Response
    #1.1. - b) If you can´t recognize any user, redirect visitor on the login page
    except:
        return redirect('login')

def SendMail(request):
    FirstName = request.POST["FirstName"]
    SecondName = request.POST["SecondName"]
    Email =  request.POST["Email"]
    Birthdate = request.POST["Birthdate"]
    Password1 = request.POST["password1"]
    Password2 = request.POST["password2"]
    if Password1==Password2:
        Token = random.randint(10**9,10**10)
        PreRegister = threading.Thread(target=Database.PreRegister,args=[FirstName, SecondName, Email, Birthdate, Password1,Token])
        PreRegister.start()

        RSM = threading.Thread(target=ReallySendMail,args=[Email,Token,FirstName,SecondName])
        RSM.start()

        return HttpResponse("Check your email")
    else:
        return redirect('registration')

def ReallySendMail(Email,Token,FirstName,OtherNames):
    AddressToCall = "http://127.0.0.1:8000/FinishReg?token=" + str(Token) + "&Email=" + Email
    Message = "Ahoj, měl by ses jmenovat " + FirstName +" "+ OtherNames + ".\n Je-li tomu tak, máš šanci se stát mým milovaným novým uživatelem a to kliknutím na tuto adresu:" + AddressToCall +  ".\n Pac a kusadlo, \nPytlík"    
    ezgmail.send(Email,"Registrace",Message)

def USRvertify(request):
    token = request.GET["token"]
    Email = request.GET["Email"]
    try:
        FirstName, OtherNames, Password, Birthdate = Database.FullRegGet(token)
    except IndexError:
        pass
    Database.KillPreReg(Email)
    return Putin(FirstName, OtherNames, Password, Birthdate,Email, request)
