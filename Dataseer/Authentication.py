import time, math, random,json, sys, os
import mysql.connector
from django.shortcuts import redirect, render
from django.template import RequestContext
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import LanguageLoader, Database,ip, Consolewriter

#After we run this on server, there will be an error with rendering pages for unsigned 

def Authenticate(request,UserID):
    token = int(str(UserID) + str(round(time.time())))
    mydb = Database.Connect()
    mycursor2 = mydb.cursor()
    IP = ip.visitor_ip_address(request)
    Command=("""INSERT INTO `Session`( Session_UserID, Session_UserToken, Session_UserDevice)
    VALUES (%s,%s,%s)""")
    VariTuple= (UserID, token, IP)
    mycursor2.execute(Command, VariTuple)
    mydb.commit()
    return token

def CheckUser(request, Page, LanguagePack):
    mydb = Database.Connect()
    TechSpy = mydb.cursor()
    try:
        token = request.COOKIES["BasicInfo"]
        Command="""SELECT Session_UserID, Session_UserDevice FROM Session WHERE Session_UserToken = %s"""
        TechSpy.execute(Command,[int(token)])
        Report = TechSpy.fetchall()
        if Report[0][1]==ip.visitor_ip_address(request):
            NewToken = int(str(Report[0][0]) + str(round(time.time())))

            NewLanguagePack, Context = BuildPack(Report[0][0], request, LanguagePack)
            Wish = render(request, Page, NewLanguagePack)
            Wish.set_cookie("BasicInfo", str(NewToken),max_age = 7200)
            Wish.set_cookie("MetaInfo", Context)

            mycursor2 = mydb.cursor()
            Command=("""UPDATE `Session` SET Session_UserToken = %s WHERE Session_UserToken =%s""")
            Continueinfo = (NewToken, token)
            mycursor2.execute(Command,Continueinfo)
            mydb.commit()

            return Wish
        else:
           LanguagePack = LanguageLoader.Language("AboutUs","Czech")
           return render(request,"Niemand\AboutUs.html", LanguagePack)
    except:
       LanguagePack = LanguageLoader.Language("AboutUs","Czech")
       return render(request,"Niemand\AboutUs.html", LanguagePack)

def QuickCheck(request):
    mydb = Database.Connect()
    TechSpy = mydb.cursor()
    try:
        token = request.COOKIES["BasicInfo"]
        Command="""SELECT Session_UserDevice FROM Session WHERE Session_UserToken = %s"""
        TechSpy.execute(Command,[int(token)])
        Report = TechSpy.fetchall()
        if Report[0]==ip.visitor_ip_address(request):
            return True
        else:
            LanguagePack = LanguageLoader.Language("AboutUs","Czech")
            return render(request,"Niemand\AboutUs.html", LanguagePack)
    except:
        LanguagePack = LanguageLoader.Language("AboutUs","Czech")
        return render(request,"Niemand\AboutUs.html", LanguagePack)


def BuildPack (ID, request, LanguagePack):
    try:
        Boolean = request.COOKIES["MetaInfo"]
        Context = 1
        return [LanguagePack, Context]
    except:
        MetaInfo = Database.ShowAll(ID)
        UserParameters = ["Contact", "FirstName", "OtherNames", "Image", "Info", "Sex", "Birthday", "Year"]
        for ParaIndex in range(0,len(UserParameters)):
            LanguagePack[UserParameters[ParaIndex]] = MetaInfo[ParaIndex]

        Context = 0
        return [LanguagePack, Context]

def GetID(request):
    mydb = Database.Connect()
    TechSpy = mydb.cursor()
    token = request.COOKIES["BasicInfo"]
    Command="""SELECT Session_UserID FROM Session WHERE Session_UserToken = %s"""
    TechSpy.execute(Command,[int(token)])
    ID = TechSpy.fetchall()[0][0]
    return ID