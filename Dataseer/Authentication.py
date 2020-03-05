import time, math, random,json, sys, os
import mysql.connector
from django.shortcuts import redirect, render
from django.template import RequestContext
import ip
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import LanguageLoader, Database

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

def CheckUser(request, Wish):
    mydb = Database.Connect()
    TechSpy = mydb.cursor()
    try:
        Cookie = request.COOKIES["BasicInfo"]
        CookieContent = json.loads(Cookie)
        token = CookieContent["token"]
        Command="""SELECT Session_UserID, Session_UserDevice FROM Session WHERE Session_UserToken = %s"""
        TechSpy.execute(Command,[token])
        Report = TechSpy.fetchall()
        if Report[0][1]==ip.visitor_ip_address(request):
            mycursor2 = mydb.cursor()
            token = int(str(Report[0][0]) + str(round(time.time())))
            Command=("""UPDATE `Session` SET Session_UserToken = %s WHERE Session_UserID = %s AND Session_UserDevice=%s""")
            Continueinfo = (token, Report[0][0], Report[0][1])
            mycursor2.execute(Command,Continueinfo)
            mydb.commit()
            CookieContent["token"] = token
            Wish.set_cookie("BasicInfo", json.dumps(CookieContent),max_age = 7200)
            return Wish
        else:
           LanguagePack = LanguageLoader.Language("HomePage","Czech")
           return render(request,"Niemand\AboutUs.html", LanguagePack)
    except:
       LanguagePack = LanguageLoader.Language("AboutUs","Czech")
       return render(request,"Niemand\AboutUs.html", LanguagePack)