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
    try:
        MyProducts = Database.GetProducts(request)
        LanguagePack["MyProducts"] = MyProducts
    except KeyError:
        pass
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

def Pasives(request):
    LanguagePack = LanguageLoader.Language("Passives","Czech")
    LanguagePack["PasivesParameters"] = Database.ShowPasives(request)
    Decision  = Authentication.CheckUser(request,"User\Passives.html",LanguagePack)
    return Decision

def NewPasives(request):
    Authentication.QuickCheck(request)
    Nickname = request.POST["Nickname"]
    Email =  request.POST["Email"]
    Info = request.POST["Info"]
    ID = int(request.COOKIES["BasicInfo"])
    ActiveID = Authentication.GetID(request)
    Database.DP6(ID,Email,Nickname,Info,ActiveID)
    return redirect('PassiveUsers')

def FindAndKill(request):
    Authentication.QuickCheck(request)
    NotToKillButToExile = request.GET["ToDelete"]
    Database.UnconnectPasive(NotToKillButToExile,request)
    return redirect('PassiveUsers')

def NewProduct(request):
    Authentication.QuickCheck(request)
    Name = request.GET["ProductName"]
    Template = request.GET["ProductTemplate"]
    ReleaseDate = request.GET["ProductRelease"]
    AbsorbationTime = request.GET["ProductAbsorbation"]
    Database.CreateProduct(request, Name, Template, ReleaseDate, AbsorbationTime)
    return redirect('Home')

def Product(request):
    LanguagePack = LanguageLoader.Language("ProductCreate","Czech")
    Decision  = Authentication.CheckUser(request,"User\ProductCreate.html",LanguagePack)  
    return Decision

def NewProductHero(request):
    Role = request.POST["ProductHero"]
    HeroName = request.POST["Nickname"]
    Database.ConnectHero(request,Role,HeroName)
    redirect('Product')