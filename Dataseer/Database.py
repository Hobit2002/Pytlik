import mysql.connector
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Consolewriter, Authentication

def Connect():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="pouhazkouska",
    database="pytlik",
    port ="3306")
    return mydb

def DP2 (q,w,e,r,t,z):
    mydb = Connect()
    mycursor2 = mydb.cursor()
    Command=("""INSERT INTO `ActiveUsers`(`ActiveUser_FirstName`,`ActiveUser_OtherNames`,`ActiveUser_Password`,
    `ActiveUser_Email`,`ActiveUser_Taste`,`ActiveUser_Year`) VALUES (%s,%s,%s,%s,%s,%s)""")
    VariTuple=(q,w,e,r,t,z)
    mycursor2.execute(Command,VariTuple)
    mydb.commit()
    Command=("""SELECT ActiveUser_ID FROM ActiveUsers
    WHERE ActiveUser_Password= %s and ActiveUser_Email= %s """)
    VariTuple=(e,r)
    mycursor2.execute(Command,VariTuple)
    W=mycursor2.fetchall()
    return W[0][0]

def DP3(q,w):
    mydb = Connect()
    mycursor2 = mydb.cursor()
    Command=("""SELECT ActiveUser_ID
                FROM ActiveUsers
                WHERE ActiveUser_Password= %s and ActiveUser_Email= %s """)
    VariTuple=(q,w)
    mycursor2.execute(Command,VariTuple)
    W=mycursor2.fetchall()

    mycursor = mydb.cursor()
    Command=("""UPDATE ActiveUsers SET ActiveUser_LastActive = now() WHERE ActiveUser_Password = %s and ActiveUser_Email = %s """)
    mycursor.execute(Command,VariTuple)
    mydb.commit()
    return W[0]

def ShowAll(ID):
    mydb = Connect()
    mycursor2 = mydb.cursor()
    Command=("""SELECT ActiveUser_Email, ActiveUser_FirstName, ActiveUser_OtherNames, ActiveUser_Image, ActiveUser_Info, ActiveUser_Sex, ActiveUser_Birthday, ActiveUser_Year
                FROM ActiveUsers
                WHERE ActiveUser_ID = %s """)
    VariTuple=[ID]
    mycursor2.execute(Command,VariTuple)
    W=mycursor2.fetchall()
    mycursor = mydb.cursor()
    Command=("""UPDATE ActiveUsers SET ActiveUser_LastActive = now() WHERE ActiveUser_ID = %s """)
    mycursor.execute(Command,VariTuple)
    mydb.commit()
    return W[0]

def UpdateUser(FirstName, SecondName, Email, Year, Info, ID):
    mydb = Connect()
    mycursor2 = mydb.cursor()
    Command=("""UPDATE ActiveUsers
               SET ActiveUser_FirstName= %s, ActiveUser_OtherNames= %s, ActiveUser_Email= %s, ActiveUser_Year= %s, ActiveUser_Info = %s         
                WHERE ActiveUser_ID = %s """)
    DataPack = (FirstName, SecondName, Email, Year, Info, ID)
    mycursor2.execute(Command,DataPack)
    mydb.commit()

def DP6(ID, Email, Nickname, Info,ActiveID):
    mydb = Connect()
    mycursor2 = mydb.cursor()
    Command="""INSERT INTO `PasiveUsers`(`PasiveUser_ID`,
    `PasiveUser_Email`,`PasiveUser_Nickname`,`PasiveUser_Info`) VALUES (%s,%s,%s,%s)"""
    DataPack = (ID, Email, Nickname, Info)
    mycursor2.execute(Command,DataPack)
    mydb.commit()
    mycursor = mydb.cursor()
    Command="""INSERT INTO `REL_ActiveUsers_PasiveUsers`(`ActiveUser_ID`,
    `PassiveUser_ID`) VALUES (%s,%s)"""
    DataPack = (ActiveID,ID)
    mycursor.execute(Command, DataPack)
    mydb.commit()

def ShowPasives(request):
    ID = Authentication.GetID(request)
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT PassiveUser_ID
            FROM REL_ActiveUsers_PasiveUsers
            WHERE ActiveUser_ID= %s """)
    VariTuple=[ID]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    mycursor2 = mydb.cursor()
    FinalResult = []
    for ToForm in Result:
        Key = ToForm[0]
        Command=("""SELECT PasiveUser_Email, PasiveUser_Nickname, PasiveUser_Info 
                FROM PasiveUsers
                WHERE PasiveUser_ID= %s """)
        VariTuple=[Key]
        mycursor2.execute(Command,VariTuple)
        Result2 = mycursor2.fetchall()
        FinalResult.append(Result2[0])
    return FinalResult

def UnconnectPasive(ToUnconnect,request):
    ID = Authentication.GetID(request)
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT PassiveUser_ID
            FROM REL_ActiveUsers_PasiveUsers
            WHERE ActiveUser_ID= %s """)
    VariTuple=[ID]
    mycursor.execute(Command,VariTuple)
    Result = mycursor.fetchall()
    mycursor2 = mydb.cursor()
    for ToForm in Result:
        Key = ToForm[0]
        Command=("""SELECT  PasiveUser_Nickname
                FROM PasiveUsers
                WHERE PasiveUser_ID= %s """)
        mycursor2.execute(Command,[Key])
        Result2 = mycursor2.fetchall()
        if Result2[0][0] == ToUnconnect:
            Breaker = mydb.cursor()
            Command ="""DELETE FROM REL_ActiveUsers_PasiveUsers WHERE PassiveUser_ID= %s"""
            Breaker.execute(Command,[Key])
            mydb.commit()

def GetProducts(request):
    ID = Authentication.GetID(request)
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT ProjectID
            FROM REL_Projects_ActiveUsers
            WHERE ActiveUserID= %s """)
    VariTuple=[ID]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    FinalResult = []
    for ToForm in Result:
        Key = ToForm[0]
        Command=("""SELECT Project_Name 
                FROM Projects
                WHERE Project_ID= %s """)
        VariTuple=[Key]
        mycursor.execute(Command,VariTuple)
        Result2 = mycursor.fetchall()
        FinalResult.append(Result2[0][0])
    return FinalResult

def GetTemplateID(Template):
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT Template_ID
            FROM Templates
            WHERE Template_Name = %s """)
    VariTuple=[Template]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    return Result[0][0]

def CreateProduct(request, Name, Template, ReleaseDate, AbsorbationTime):
    mydb = Connect()
    mycursor = mydb.cursor()
    Command="""INSERT INTO `Projects`(`Project_Name`,
    `Project_Template`, Project_Release, Project_AbsorbTime) VALUES (%s,%s,%s,%s)"""
    TemplateID = GetTemplateID(Template)
    VariTuple=[Name, TemplateID, ReleaseDate, AbsorbationTime]
    mycursor. execute(Command,VariTuple)
    mydb.commit()
    LateAgent = mydb.cursor()
    Command=("""SELECT Project_ID
            FROM Projects
            WHERE Project_Name = %s AND `Project_Template`= %s AND Project_Release= %s AND Project_AbsorbTime= %s""")
    VariTuple=[Name, TemplateID, ReleaseDate, AbsorbationTime]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    ProjectID = Result[0][0]
    UserID = Authentication.GetID(request)
    Command="""INSERT INTO `REL_Projects_ActiveUsers`(`ProjectID`,
    `ActiveUserID`, RelationType) VALUES (%s,%s,%s)"""
    IDs = [ProjectID,UserID,'Boss']
    mycursor. execute(Command,IDs)
    mydb.commit()
    return ProjectID

def ShowHeroes(ProductName):
    Team = []
    Clients = []
    ProductID = GetProductID(ProductName)
    mydb = Connect()
    mycursor = mydb.cursor()
    #Pasive Users
    Command=("""SELECT PasiveUserID, RelationType
            FROM REL_Projects_PasiveUsers
            WHERE ProjectID= %s """)
    VariTuple=[ProductID]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    mycursor2 = mydb.cursor()
    for ToForm in Result:
        Key = ToForm[0]
        RelationType = str(ToForm[1])
        Command=("""SELECT PasiveUser_Nickname 
                FROM PasiveUsers
                WHERE PasiveUser_ID= %s """)
        VariTuple=[Key]
        mycursor2.execute(Command,VariTuple)
        Result2 = (mycursor2.fetchall())[0][0]
        if RelationType == "{'TeamMember'}":
            Team.append(Result2)
        elif RelationType == "{'Client'}":
            Clients.append(Result2)
    #Same things for active
    Command=("""SELECT ActiveUserID, RelationType
            FROM REL_Projects_ActiveUsers
            WHERE ProjectID= %s """)
    VariTuple=[ProductID]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    mycursor2 = mydb.cursor()
    for ToForm in Result:
        Key = ToForm[0]
        RelationType = str(ToForm[1])
        Command=("""SELECT CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames) 
                FROM ActiveUsers
                WHERE ActiveUser_ID= %s """)
        VariTuple=[Key]
        mycursor2.execute(Command,VariTuple)
        Result2 = (mycursor2.fetchall())[0][0]
        if RelationType == "{'TeamMember'}":
            Team.append(Result2)
        elif RelationType == "{'Client'}":
            Clients.append(Result2)
    return [Team,Clients]

def GetProductID(ProductName):
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT Project_ID
            FROM Projects
            WHERE Project_Name = %s """)
    VariTuple=[ProductName]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    return Result[0][0]

def ConnectHero(request,Role,HeroName,ProductName):
    UserID = Authentication.GetID(request)
    ProductID = GetProductID(ProductName)
    mydb = Connect()
    mycursor = mydb.cursor()
    PartialCommand="""SELECT PassiveUser_ID 
                FROM REL_ActiveUsers_PasiveUsers
                WHERE ActiveUser_ID =""" + str(UserID)
    mycursor.execute(PartialCommand)
    PassiveList = mycursor.fetchall()
    SmoothList = ""
    for ListPart in PassiveList:
        SmoothList = SmoothList +", " + str(ListPart[0])
        SmoothList = SmoothList[1:]
    MainCommand = """SELECT PasiveUser_ID
                   FROM PasiveUsers
                    WHERE  PasiveUser_Nickname = %s AND
                    PasiveUser_ID IN (""" + SmoothList + """)"""
    VariTuple = [HeroName]
    mycursor.execute(MainCommand,VariTuple)
    Statement = mycursor.statement
    Result = mycursor.fetchall()
    try:
        DerivatedResult = int(Result[0][0])
        TeamInsertor = mydb.cursor()
        INScommand = """INSERT INTO REL_Projects_PasiveUsers(ProjectID, PasiveUserID, RelationType) VALUES (%s,%s,%s)"""
        Values = [ProductID,DerivatedResult,Role]
        TeamInsertor.execute(INScommand,Values)
        mydb.commit()
    except IndexError:
        ActiveSelector = mydb.cursor()
        MainCommand = """SELECT ActiveUser_ID
                   FROM ActiveUsers
                    WHERE  CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames) = %s"""
        ActiveSelector.execute(MainCommand,[HeroName])
        ActiveUserID = ActiveSelector.fetchall()[0][0]
        TeamInsertor = mydb.cursor()
        INScommand = """INSERT INTO REL_Projects_ActiveUsers(ProjectID, ActiveUserID, RelationType) VALUES (%s,%s,%s)"""
        Values = [ProductID,ActiveUserID,Role]
        TeamInsertor.execute(INScommand,Values)
        mydb.commit()

def UnconnectHero(Role,HeroName,ProductName):
    ProductID = GetProductID(ProductName)
    mydb = Connect()
    mycursor = mydb.cursor()
    PartialCommand="""SELECT PasiveUserID 
                FROM REL_Projects_PasiveUsers
                WHERE ProjectID =""" + str(ProductID)
    Consolewriter.ShowInConsole(PartialCommand)
    mycursor.execute(PartialCommand)
    PassiveList = mycursor.fetchall()
    SmoothList = ""
    Consolewriter.ShowInConsole(PassiveList)
    for ListPart in PassiveList:
        SmoothList = SmoothList +", " + str(ListPart[0])
        SmoothList = SmoothList[1:]
    Consolewriter.ShowInConsole(SmoothList)
    MainCommand = """SELECT PasiveUser_ID
                   FROM PasiveUsers
                    WHERE  PasiveUser_Nickname = %s AND
                    PasiveUser_ID IN (""" + SmoothList + ")"
    VariTuple = [HeroName]
    mycursor.execute(MainCommand,VariTuple)
    Statement = mycursor.statement
    Result = mycursor.fetchall()
    try:
        DerivatedResult = int(Result[0][0])
        TeamInsertor = mydb.cursor()
        DELcommand = """DELETE FROM REL_Projects_PasiveUsers 
                        WHERE ProjectID = %s AND PasiveUserID = %s AND RelationType = %s"""
        Values = [int(ProductID),DerivatedResult,Role]
        TeamInsertor.execute(DELcommand,Values)
        mydb.commit()
    except IndexError:
        ActiveSelector = mydb.cursor()
        MainCommand = """SELECT ActiveUser_ID
                   FROM ActiveUsers
                    WHERE  CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames) = %s"""
        ActiveSelector.execute(MainCommand,[HeroName])
        ActiveUserID = ActiveSelector.fetchall()[0][0]
        TeamInsertor = mydb.cursor()
        DELcommand = """DELETE FROM REL_Projects_ActiveUsers
                        WHERE ProjectID=%s AND ActiveUserID=%s AND RelationType=%s"""
        Values = [ProductID,ActiveUserID,Role]
        TeamInsertor.execute(DELcommand,Values)
        mydb.commit()



        
