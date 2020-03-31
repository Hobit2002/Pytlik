from django.shortcuts import render, redirect
from django.template import RequestContext
import json, re,time,sys,os, time,os, datetime
from pathlib import Path
from django.urls import path, reverse
from django.utils.datastructures import MultiValueDictKeyError
from urllib.parse import urlencode
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Authentication, Database, LanguageLoader, Consolewriter
from django.http import HttpResponseRedirect
# Create your views here.

def Home(request):
    LanguagePack = LanguageLoader.Language("HomePage","Czech")
    try:
        MyProducts = Database.GetProducts(request)
        LanguagePack["MyProducts"] = MyProducts
    except KeyError:
        pass
    LanguagePack["Identity"] = "Me"
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
    Birthday = request.POST["Birthday"]
    ID = Authentication.GetID(request)
    Database.UpdateUser(FirstName, SecondName, Email, Year, Info, Sex, Birthday, ID)
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
    #Load Basics
    LanguagePack = LanguageLoader.Language("ProductCreate","Czech")
    ProductName = request.GET["OldProductName"]
    BaseNameForm = re.compile(r'(.*)ßđ€9@' )
    BaseNameQuest = BaseNameForm.search(ProductName)
    BasicName = BaseNameQuest.group()
    PublicProductName = BasicName[:(len(BasicName)-5)]
    LanguagePack["ProductName"] = ProductName
    LanguagePack["PublicProductName"] = PublicProductName
    #Load Team
    Team, Clients = Database.ShowHeroes(ProductName)
    LanguagePack["Clients"] = Clients
    LanguagePack["TeamMembers"] = Team
    #Load Tasks
    Tasks = Database.ShowTasks(ProductName)
    LanguagePack["Tasks"] = Tasks
    #Load Role
    VisitorRole = Database.VisitorRole(ProductName,request)
    LanguagePack["VisitorRoles"] = VisitorRole
    #GoToPage
    Decision  = Authentication.CheckUser(request,"User\ProductCreate.html",LanguagePack)  
    return Decision

def NewProductHero(request):
    Authentication.QuickCheck(request)
    StringData = request.POST["ProductHero"]
    StringData = StringData.replace("\'", "\"")
    ProductHero = json.loads(StringData)
    Role = ProductHero["Role"]
    HeroName = request.POST["Nickname"]
    ProductName = ProductHero["ProductName"]
    Database.ConnectHero(request,Role,HeroName,ProductName)
    URL = CallProduct(ProductName)
    return redirect(URL)

def DeleteHero(request):
    StringData = request.GET["ToDelete"]
    StringData = StringData.replace("\'", "\"")
    ProductHero = json.loads(StringData)
    Role = ProductHero["Role"]
    HeroName = ProductHero["ExheroName"]
    ProductName = ProductHero["ProductName"]
    if Database.CheckBoss(request,ProductName):
        Database.UnconnectHero(Role = Role,HeroName = HeroName,ProductName = ProductName)
        URL = CallProduct(ProductName)
        return redirect(URL)
    else:
        return redirect('Home') 

def SelfDeleteHero(request):
    StringData = request.GET["ToDelete"]
    StringData = StringData.replace("\'", "\"")
    ProductHero = json.loads(StringData)
    Role = ProductHero["Role"]
    HeroID = Authentication.GetID(request)
    ProductName = ProductHero["ProductName"]
    Database.UnconnectHero(Role = Role,HeroID = HeroID,ProductName = ProductName)
    URL = CallProduct(ProductName)
    return redirect(URL)

def DeleteTask(request):
    Authentication.QuickCheck(request)
    StringData = request.GET["ToDelete"]
    StringData = StringData.replace("\'", "\"")
    DyingTask = json.loads(StringData)
    TaskName = DyingTask["TaskName"]
    ProductName = DyingTask["ProductName"]
    Database.DeleteTask(TaskName,ProductName)
    URL = CallProduct(ProductName)
    return redirect(URL)

def CallProduct(ProductName):
    base_url = reverse('Product')
    query_string =  urlencode({'OldProductName': ProductName})
    url = '{}?{}'.format(base_url, query_string)
    return url

def NewTask(request):
    Authentication.QuickCheck(request)
    ProductName = request.GET["ProductName"]
    TaskName = request.GET["TaskName"]
    HeroName = request.GET["HeroName"]
    Deadline = request.GET["Deadline"]
    WorkTime = request.GET["WorkTime"]
    Database.CreateTask(ProductName,TaskName,HeroName,Deadline,WorkTime, True, request)
    URL = CallProduct(ProductName)
    return redirect(URL)

def DeleteProduct(request):
    ProductName = request.GET["ProductName"]
    if Database.CheckBoss(request,ProductName):
        Database.DeleteProduct(ProductName)
        URL = CallProduct(ProductName)

    return redirect('Home')

def NewTaskHero(request):
    StringData = request.GET["ExtraValues"]
    StringData = StringData.replace("\'", "\"")
    ComingHeroCoordinates = json.loads(StringData)
    TaskName = ComingHeroCoordinates["TaskName"]
    ProductName = ComingHeroCoordinates["ProductName"]
    NewTaskHero = request.GET["NewTaskHero"]
    if Database.CheckBoss(request,ProductName):
        Database.AddTaskHero(ProductName,TaskName,NewTaskHero,request)
        URL = CallProduct(ProductName)
        return redirect(URL)
    else:
        return redirect('Home')

def DeleteTaskHero(request):
    StringData = request.GET["ToDelete"]
    StringData = StringData.replace("\'", "\"")
    DyingTask = json.loads(StringData)
    TaskName = DyingTask["TaskName"]
    ProductName = DyingTask["ProductName"]
    HeroIndex = int(DyingTask["HeroIndex"])
    if Database.CheckBoss(request,ProductName):
        Database.DeleteTaskHero(TaskName,HeroIndex)
        URL = CallProduct(ProductName)
        return redirect(URL)
    else:
        return redirect('Home')

def ResetTaskTime(request):
    Deadline = request.GET["Deadline"]
    WorkTime = request.GET["WorkTime"]
    StringData = request.GET["TaskIdentificators"]
    StringData = StringData.replace("\'", "\"")
    DyingTask = json.loads(StringData)
    TaskName = DyingTask["TaskName"]
    ProductName = DyingTask["ProductName"]
    if Database.CheckBoss(request,ProductName):
        Database.UpdateTaskTime(Deadline,WorkTime,TaskName)
        URL = CallProduct(ProductName)
        return redirect(URL)
    else:
        return redirect('Home')

def Search(request):
    Authentication.QuickCheck(request)
    Wanted = request.GET["LookForThis"]
    Employee = Database.LookForUser(Wanted)
    if Employee != []:
        ID, Name, Birthday,Sex, Info = Employee[0]
        LanguagePack = LanguageLoader.Language("HomePage","Czech")
        SearchedUserPack = {"Name_Search":Name, "Birthday_Search":Birthday,"Sex_Search":LanguageLoader.LoadWord(str(Sex), "Czech"), "Info_Search":Info}
        LanguagePack["SearchUsr"] = SearchedUserPack
        Products = Database.GetProducts(request, ID)
        LanguagePack["MyProducts"] = Products
        LanguagePack["Identity"] = "Visitor"
        return render (request,"User\HomePage.html",LanguagePack)

def Diary(request):
    LanguagePack = LanguageLoader.Language("Diary","Czech")
    DiaryData = open('Dataseer\Chapters.json','r')
    ReDiDa = json.load(DiaryData)
    DiaryData.close()
    LanguagePack["DiaryData"] = ReDiDa
    LanguagePack["Templates"] = Database.GetiDiaryTemplates(request)
    #GoToPage
    Decision  = Authentication.CheckUser(request,"User\Diary.html",LanguagePack)  
    return Decision

def SubmitDiary(request):
    DiaryData = open('Dataseer\Chapters.json','r')
    ReDiDa = json.load(DiaryData)
    NewTemCom = request.GET["NewTemplate"]
    TemplateChapters = []
    SubmitFormat = request.GET["Savingformat"]
    if SubmitFormat != '':
        Database.DeleteDayChapters(request,SubmitFormat)
    try:
        Overall = request.GET["TypeOfActivity"]
        Overall = json.loads(Overall)
        Overall = Overall["Python"]
        PropertiesNames = ReDiDa["Activities"][Overall]
        DatabaseJSON = {}
        DatabaseJSON["TypeOfActivity"] = Overall
        for LoopIdx,Property in enumerate(PropertiesNames):
            if type(Property) == list:
                ListProperty = request.GET[Property[1]]
                JSONkey = "Concretly" + str(LoopIdx)
                DatabaseJSON[JSONkey] = ListProperty
            elif type(Property) == str:
                Quality = request.GET[Property]
                DatabaseJSON[Property] = Quality
        Emotions = ReDiDa["Emotions"]
        for Emotion in Emotions:
            DatabaseJSON[Emotion] = request.GET[Emotion]
        ActivityStart = request.GET["StartTime"]
        DatabaseJSON["ActivityStart"]  = ActivityStart
        ActivityEnd = request.GET["EndTime"]
        DatabaseJSON["ActivityEnd"] = ActivityEnd
        ID = Database.InsertChapter(json.dumps(DatabaseJSON), request, ActivityStart,ActivityEnd)
        TemplateChapters.append(ID)
    except MultiValueDictKeyError:
        pass

    AddedChapters = int(request.GET["AddChaptersCount"])
    for i in range(1,AddedChapters+1):
        try:
            Overall = request.GET["TypeOfActivity"+str(i)]
            Overall = json.loads(Overall)
            Overall = Overall["Python"]
            PropertiesNames = ReDiDa["Activities"][Overall]
            DatabaseJSON = {}
            DatabaseJSON["TypeOfActivity"] = Overall
            for LoopIdx,Property in enumerate(PropertiesNames):
                if type(Property) == list:
                    ListProperty = request.GET[Property[1]+str(i)]
                    JSONkey = "Concretly" + str(LoopIdx)
                    DatabaseJSON[JSONkey] = ListProperty
                elif type(Property) == str:
                    Quality = request.GET[Property+str(i)]
                    DatabaseJSON[Property] = Quality
            Emotions = ReDiDa["Emotions"]
            for Emotion in Emotions:
                DatabaseJSON[Emotion] = request.GET[Emotion+str(i)]
            ActivityStart = request.GET["StartTime"+str(i)]
            DatabaseJSON["ActivityStart"]  = ActivityStart
            ActivityEnd = request.GET["EndTime"+str(i)]
            DatabaseJSON["ActivityEnd"] = ActivityEnd
            ID = Database.InsertChapter(json.dumps(DatabaseJSON), request, ActivityStart,ActivityEnd)
            TemplateChapters.append(ID)
        except MultiValueDictKeyError:
            pass
    DiaryData.close()
    if str(NewTemCom) =="1":
        TemplateName = request.GET["NewTemplateName"]
        TemplateName = TemplateName + "Q"+ str(round(time.time()))
        Database.InsertChapterTemplate(request,TemplateChapters,TemplateName)
    ReturnSpace = request.GET["CurrentURL"]
    return redirect(ReturnSpace)

def HeroSelfInclude(request):
    ProductName = request.GET["ProductName"]
    HeroID = Authentication.GetID(request)
    ProductID = Database.GetProductID(ProductName)
    Database.CreateHeroProductConnection(ProductID,HeroID,'Client')
    URL = CallProduct(ProductName)
    return redirect(URL)

def Calendar(request):
    RawDate = json.loads(request.GET["CurrentMonth"])
    Month = int(RawDate["Month"]) + 1
    Year = int(RawDate["Year"])
    Weekday = (datetime.date(Year,Month,1)).weekday() + 1
    MonthLen = (datetime.date(Year,Month + 1,1) - datetime.date(Year,Month,1)).days
    MonthDays = []
    for Day in range(1,MonthLen+1):
        MonthDays.append(Day)
 
    LanguagePack = LanguageLoader.Language("Calendar","Czech")
    LanguagePack["Weekday"] = Weekday
    LanguagePack["WeekRadio"] = [1,2,3,4,5,6,7]
    LanguagePack["MonthDays"] = MonthDays
    LanguagePack["Month"] = Month
    LanguagePack["Year"] = Year
    Decision  = Authentication.CheckUser(request,"User\Calendar.html",LanguagePack)  
    return Decision

def CallDay(request):
    LanguagePack = LanguageLoader.Language("Diary","Czech")
    DiaryData = open('Dataseer\Chapters.json','r')
    ReDiDa = json.load(DiaryData)
    DiaryData.close()
    LanguagePack["DiaryData"] = ReDiDa
    LanguagePack["Templates"] = Database.GetiDiaryTemplates(request)
    #Get right day
    Json = request.GET["CalledDate"]
    Date = json.loads(Json.replace("\'","\""))
    Day = int(Date["Day"])
    Month = int(Date["Month"])
    Year = int(Date["Year"])
    FullDate = datetime.date(Year,Month,Day)
    LanguagePack["Date"] = str(FullDate)
    LanguagePack["DayHistory"] = Database.StoriesOfPast(request,FullDate)
    #GoToPage
    LanguagePack["Role"] = "Memory"
    Decision  = Authentication.CheckUser(request,"User\Diary.html",LanguagePack)  
    return Decision