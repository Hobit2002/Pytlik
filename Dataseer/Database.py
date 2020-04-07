import mysql.connector
import sys,os, json, re, time, datetime
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Consolewriter, Authentication, LanguageLoader

def Connect():
    mydb = mysql.connector.connect(
    host="bejt.local",
    user="pytlikapp",
    passwd="Trochu-KRATS-190",
    database="pytlik",
    port ="3307")
    return mydb

def PreRegister(FirstName, SecondName, Email, Birthdate, Password, Token):
    mydb = Connect()
    mycursor2 = mydb.cursor()
    Command="""INSERT INTO PreRegistred(PreRegistred_FirstName, PreRegistred_OtherNames, PreRegistred_Password, PreRegistred_Birthdate,
    PreRegistred_Email, PreRegistred_Token) VALUES (%s,%s,%s,%s,%s,%s)"""
    VariTuple=[FirstName, SecondName, Password,Birthdate,Email, Token]
    mycursor2.execute(Command,VariTuple)
    mydb.commit()

def FullRegGet(token):
    Shire = Connect()
    Bilbo = Shire.cursor()
    UnexpectedJounuery= """SELECT PreRegistred_FirstName, PreRegistred_OtherNames, PreRegistred_Password, PreRegistred_Birthdate
                        FROM PreRegistred WHERE PreRegistred_Token = %s"""
    Bilbo.execute(UnexpectedJounuery,[token])
    DragonTreasure = Bilbo.fetchall()[0]
    return DragonTreasure

def KillPreReg(Email):
    ShadowShire = Connect()
    DarkBilbo = ShadowShire.cursor()
    MordorQuest = """DELETE
                    FROM PreRegistred WHERE PreRegistred_Email = %s"""
    DarkBilbo.execute(MordorQuest,[Email])
    ShadowShire.commit()

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

def UpdateUser(FirstName, SecondName, Email, Year, Info,Sex, Birthday, ID):
    mydb = Connect()
    mycursor2 = mydb.cursor()
    Command=("""UPDATE ActiveUsers
               SET ActiveUser_FirstName= %s, ActiveUser_OtherNames= %s, ActiveUser_Email= %s, ActiveUser_Year= %s, ActiveUser_Info = %s, ActiveUser_Sex = %s, ActiveUser_Birthday = %s         
                WHERE ActiveUser_ID = %s """)
    DataPack = (FirstName, SecondName, Email, Year, Info, Sex, Birthday, ID)
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

def GetProducts(request, ID=""):
    if not ID:
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
    FullNames = []
    for ToForm in Result:
        Key = ToForm[0]
        Command=("""SELECT Project_Name 
                FROM Projects
                WHERE Project_ID= %s """)
        VariTuple=[Key]
        mycursor.execute(Command,VariTuple)
        Result2 = mycursor.fetchall()[0][0]
        if Result2 not in FullNames:
            FullNames.append(Result2)
            BaseNameForm = re.compile(r'(.*)ßđ€9@' )
            BaseNameQuest = BaseNameForm.search(Result2)
            BasicName = BaseNameQuest.group()
            BasicName = BasicName[:(len(BasicName)-5)]
            ProductPack = {"BasicName":BasicName, "DatabaseName":Result2}
            FinalResult.append(ProductPack)
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
    token = request.COOKIES["BasicInfo"]
    Name = Name +"ßđ€9@"+str(token)
    Command="""INSERT INTO `Projects`(`Project_Name`,
    `Project_Template`, Project_Release, Project_AbsorbTime) VALUES (%s,%s,%s,%s)"""
    TemplateID = GetTemplateID(Template)
    VariTuple=[Name, TemplateID, ReleaseDate, AbsorbationTime]
    mycursor. execute(Command,VariTuple)
    mydb.commit()
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
    mycursor.execute(Command,IDs)
    mydb.commit()
    #Set up tasks
    TaskSelector = mydb.cursor()
    Command=("""SELECT Template_Tasks
            FROM Templates
            WHERE Template_Name = %s""")
    VariTuple=[Template]
    TaskSelector.execute(Command,VariTuple)
    RawString = (TaskSelector.fetchall())[0][0]
    Tasks = json.loads(RawString)
    for Task in Tasks:
        TaskInsertor = mydb.cursor()
        Command = """INSERT INTO Tasks(Project_ID, Task_Content, TasK_Deadline) VALUES(%s, %s, %s)"""
        Values = [ProjectID, Task, ReleaseDate]
        TaskInsertor.execute(Command,Values)
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

def GetProjectID(ProjectName):
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT RealProject_ID
            FROM RealProjects
            WHERE RealProject_Name = %s """)
    VariTuple=[ProjectName]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    return Result[0][0]

def ConnectHero(request,Role,HeroName,ProductName,URL):
    UserID = Authentication.GetID(request)
    ProductID = GetProductID(ProductName)
    mydb = Connect()
    mycursor = mydb.cursor()
    PartialCommand="""SELECT PassiveUser_ID 
                FROM REL_ActiveUsers_PasiveUsers
                WHERE ActiveUser_ID =""" + str(UserID)
    mycursor.execute(PartialCommand)
    PassiveList = mycursor.fetchall()
    SmoothList = str(PassiveList[0][0])
    for ListPart in PassiveList[1:]:
        SmoothList = SmoothList +", " + str(ListPart[0])
    if len(SmoothList)>1:
        MainCommand = """SELECT PasiveUser_ID
                       FROM PasiveUsers
                        WHERE  PasiveUser_Nickname = %s AND
                        PasiveUser_ID IN (""" + SmoothList + """)"""
        VariTuple = [HeroName]
        mycursor.execute(MainCommand,VariTuple)
        Statement = mycursor.statement
        Result = mycursor.fetchall()
    else:
        Result = ""
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
        if Role == "TeamMember":
            #Send Notification
            BaseNameForm = re.compile(r'(.*)ß' )
            BaseNameQuest = BaseNameForm.search(ProductName)
            BasicName = BaseNameQuest.group()
            BasicName = BasicName[:(len(BasicName)-1)]
            Content = LanguageLoader.LoadWord("ProductTeamNTF","Czech") + BasicName
            SendNotification(ActiveUserID,Content,BasicName,URL)

        CreateHeroProductConnection(ProductID,ActiveUserID,Role)

def CreateHeroProductConnection(ProductID,ActiveUserID,Role):
    mydb = Connect()
    TeamInsertor = mydb.cursor()
    INScommand = """INSERT INTO REL_Projects_ActiveUsers(ProjectID, ActiveUserID, RelationType) VALUES (%s,%s,%s)"""
    Values = [ProductID,ActiveUserID,Role]
    TeamInsertor.execute(INScommand,Values)
    mydb.commit()

def UnconnectHero(Role,ProductName,HeroName="", HeroID=""):
    ProductID = GetProductID(ProductName)
    mydb = Connect()
    mycursor = mydb.cursor()
    #Self delete
    if HeroID != "":
        TeamInsertor = mydb.cursor()
        DELcommand = """DELETE FROM REL_Projects_ActiveUsers
                        WHERE ProjectID=%s AND ActiveUserID=%s AND RelationType=%s"""
        Values = [ProductID,HeroID,Role]
        TeamInsertor.execute(DELcommand,Values)
        mydb.commit()
        return True
    #Delete by Boss
    PartialCommand="""SELECT PasiveUserID 
                FROM REL_Projects_PasiveUsers
                WHERE ProjectID =""" + str(ProductID)
    mycursor.execute(PartialCommand)
    PassiveList = mycursor.fetchall()
    SmoothList = str(PassiveList[0][0])
    for ListPart in PassiveList[1:]:
        SmoothList = SmoothList +", " + str(ListPart[0])
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

def ShowTasks(ProductName):
    ProductID = GetProductID(ProductName)
    mydb = Connect()
    mycursor = mydb.cursor()
    PartialCommand="""SELECT Task_Content, Hero_ID, Hero_Nature,Task_WorkTime, Task_Deadline
                FROM Tasks
                WHERE Project_ID =""" + str(ProductID) + """ ORDER BY Task_DeadLine"""
                
    mycursor.execute(PartialCommand)
    TaskList = mycursor.fetchall()
    ToSend = []
    SetUpTasks = []
    for AppendMaterial in TaskList:
        RealTask = AppendMaterial[0]
        if RealTask not in SetUpTasks:
            SetUpTasks.append(RealTask)
            ToSend.append({})
            UpdatedDict = ToSend[(len(ToSend)-1)]
            #Insert task content
            Task = LanguageLoader.LoadTaskName(RealTask, "Czech")
            UpdatedDict["Task"] = Task
            UpdatedDict["RealTask"] = RealTask
            UpdatedDict["Hero"] = []
            UpdatedDict["WorkTime"] = str(AppendMaterial[3])
            UpdatedDict["Deadline"] = (str(AppendMaterial[4])[:(len(str(AppendMaterial[4]))-3)]).replace(" ","T")
        else:
            UpdatedDict = ToSend[SetUpTasks.index(RealTask)]

            #Insert hero
        Samuel = mydb.cursor()
        BlessedLocation = AppendMaterial[2]
        HeroID = AppendMaterial[1]
        if str(BlessedLocation) == "{'Pasive'}":
            ProphetMission = """SELECT PasiveUser_Nickname
                                 FROM PasiveUsers
                                 WHERE PasiveUser_ID=%s"""
            Samuel.execute(ProphetMission, [HeroID])
            Kings = Samuel.fetchall()
            KingDavid = Kings[0][0]
            UpdatedDict["Hero"].append(KingDavid)
        elif str(BlessedLocation) =="{'Active'}":
            ProphetMission = """SELECT CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames)
                                FROM ActiveUsers
                                WHERE ActiveUser_ID=%s"""
            Samuel.execute(ProphetMission, [HeroID])
            Kings = Samuel.fetchall()
            KingSaul = Kings[0][0]
            UpdatedDict["Hero"].append(KingSaul)
    return ToSend

def DeleteTask(TaskName,ProductName):
    mydb = Connect()
    LazyGuy = mydb.cursor()
    DELcommand = """DELETE FROM Tasks 
                    WHERE Task_Content = %s"""
    LazyGuy.execute(DELcommand,[TaskName])
    mydb.commit()
    return True

def GetTaskID(TaskName,ProductName):
    ProductID = GetProductID(ProductName)
    mydb = Connect()
    mycursor = mydb.cursor()
    Command = """SELECT Task_ID
                  FROM Tasks
                  WHERE Task_Content = %s AND Project_ID = %s"""
    Values = [TaskContent, ProductID]
    mycursor.execute(Command,Values)
    TaskID = mycursor.fetchall()
    return TaskID[0][0]

def CreateTask(ProductName,TaskName,HeroName,Deadline,WorkTime, Alter, request=''):
    ProductID = GetProductID(ProductName)
    #If the task hasn´t exist yet, create him a database name.
    if Alter:
        DatabaseName = TaskName + "l" + str(ProductID)+str(time.time())
        DatabaseName = DatabaseName.replace(".","d")
        LanguageLoader.AddToDatactionary("Czech",DatabaseName,TaskName)
        TaskName = DatabaseName
    #If the task hasn´t exist yet, create him a blank representation in database.
        mydb=Connect()
        Leonardo = mydb.cursor()
        ArtVision = """INSERT INTO Tasks(Project_ID,Task_Content, Task_Deadline, Task_WorkTime)
                       VALUES(%s,%s,%s,%s)"""
        Values=[ProductID, TaskName,Deadline,WorkTime]
        Leonardo.execute(ArtVision,Values)
        mydb.commit()
    if HeroName != None: 
        #Investigate, if HeroName referes to Active or Pasive user
        #References connected pasive user?
        mydb = Connect()
        mycursor = mydb.cursor()
        PartialCommand="""SELECT PasiveUserID 
                FROM REL_Projects_PasiveUsers
                WHERE ProjectID =""" + str(ProductID)
        mycursor.execute(PartialCommand)
        PassiveList = mycursor.fetchall()
        SmoothList = str(PassiveList[0][0])
        for ListPart in PassiveList[1:]:
            SmoothList = SmoothList +", " + str(ListPart[0])
        Holmes = mydb.cursor()
        Command = """SELECT PasiveUser_ID
                 FROM PasiveUsers
                 WHERE PasiveUser_Nickname = %s AND PasiveUser_ID IN (""" + SmoothList + """)"""
        Holmes.execute(Command, [HeroName])
        HolmesStatement = Holmes.statement
        Result = Holmes.fetchall()
        #References connected active user?
        if Result==[] and HeroName!="":
            Poirot = mydb.cursor()
            MainCommand = """SELECT ActiveUser_ID
                   FROM ActiveUsers
                    WHERE  CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames) = %s"""
            Poirot.execute(MainCommand,[HeroName])
            Result = Poirot.fetchall()
            #References unconnected pasive user?
            if Result == []:
                UserID = Authentication.GetID(request)
                UserHerald = mydb.cursor()
                SocialMission= """SELECT PassiveUser_ID 
                FROM REL_ActiveUsers_PasiveUsers
                WHERE ActiveUser_ID =""" + str(UserID)
                UserHerald.execute(SocialMission)
                PassiveList = UserHerald.fetchall()
                SmoothList = str(PassiveList[0][0])
                for ListPart in PassiveList[1:]:
                    SmoothList = SmoothList +", " + str(ListPart[0])
                Holmes = mydb.cursor()
                Command = """SELECT PasiveUser_ID
                 FROM PasiveUsers
                 WHERE PasiveUser_Nickname = %s AND PasiveUser_ID IN (""" + SmoothList + """)"""
                Holmes.execute(Command, [HeroName])
                Result = Holmes.fetchall()
                ConnectHero(request,'TeamMember',HeroName,ProductName)
                ID = Result[0][0]
                Nature = "Pasive"

            else:
                ID = Result[0][0]
                Nature = "Active"

        elif len(Result)==1:
            ID = Result[0][0]
            Nature = "Pasive"
        elif HeroName == "":
            ID =""
            Nature=""
        

        Leonardo = mydb.cursor()
        ArtVision = """INSERT INTO Tasks(Project_ID,Task_Content,Hero_ID, Hero_Nature, Task_Deadline, Task_WorkTime)
                   VALUES(%s,%s,%s,%s,%s,%s)"""
        Values=[ProductID, TaskName,ID,Nature,Deadline,WorkTime]
        Leonardo.execute(ArtVision,Values)
        mydb.commit()

def VisitorRole(ProductName,request):
    try:
        UserID = Authentication.GetID(request)
    except KeyError:
        UserRole = "DubiousStranger"
        return UserRole

    ProductID = GetProductID(ProductName)
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT RelationType
            FROM REL_Projects_ActiveUsers
            WHERE ProjectID= %s AND ActiveUserID =%s""")
    VariTuple=[ProductID,UserID]
    mycursor.execute(Command,VariTuple)
    Result = mycursor.fetchall()
    Roles = []
    if Result != []:
        Roles = []
        for Role in Result:
            Roles.append(str(Role[0]))
        UserRole = Roles
    else:
        UserRole = "DubiousStranger"
    return UserRole

def CheckBoss(request, ProductName):
    VisitorRoles = VisitorRole(ProductName,request)
    if "{'Boss'}" in VisitorRoles:
        return True
    else:
        return False

def DeleteProduct(ProductName):
    ProdID = GetProductID(ProductName)
    mydb = Connect()
    BurnoutGuy = mydb.cursor()
    DELcommand = """DELETE FROM Projects 
                    WHERE Project_ID = %s"""
    BurnoutGuy.execute(DELcommand,[ProdID])
    mydb.commit()
    return True

def AddTaskHero(ProductName,TaskName,NewTaskHero,request=''):
    #Get task times
    mydb = Connect()
    ShowLeader = mydb.cursor()
    Command = """SELECT Task_Deadline,Task_WorkTime
                 FROM Tasks
                 WHERE Task_Content = %s"""
    ShowLeader.execute(Command,[TaskName])
    Result = ShowLeader.fetchall()[0]
    Deadline = Result[0]
    WorkTime = Result[1]
    # Insert new team collaborator
    CreateTask(ProductName,TaskName,NewTaskHero,Deadline,WorkTime,False,request)

def DeleteTaskHero(TaskName,HeroIndex):
    mydb=Connect()
    HeroTrairor = mydb.cursor()
    RotIdea = """SELECT Task_ID 
                 FROM Tasks
                 WHERE Task_Content = %s
                 ORDER BY Task_Deadline"""
    HeroTrairor.execute(RotIdea,[TaskName])
    TaskID = HeroTrairor.fetchall()[HeroIndex][0]
    HeroSlayer = mydb.cursor()
    HuntMotto = """DELETE FROM Tasks
                  WHERE Task_ID = %s"""
    HeroSlayer.execute(HuntMotto,[TaskID])
    mydb.commit()

def UpdateTaskTime(Deadline,WorkTime,TaskName):
    mydb=Connect()
    Reformator = mydb.cursor()
    Statement = """UPDATE Tasks
                   SET Task_WorkTime = %s, Task_Deadline = %s
                   WHERE  Task_Content = %s"""
    Inspiration = [WorkTime,Deadline,TaskName]
    Reformator.execute(Statement,Inspiration)
    mydb.commit()

def LookForUser(Wanted):
    mydb = Connect()
    HeadHunter = mydb.cursor()
    Instructions = """SELECT ActiveUser_ID, CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames), ActiveUser_Birthday,ActiveUser_Sex, ActiveUser_Info
                     FROM ActiveUsers
                     WHERE CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames) LIKE %s"""
    AgentCloak = ["%" + Wanted + "%"]
    HeadHunter.execute(Instructions, AgentCloak)
    Boss = HeadHunter.fetchall()
    return Boss

def InsertChapter(DatabaseJSON, request,ActivityStart,ActivityEnd):
    UserID = Authentication.GetID(request)
    BilboHouse = Connect()
    Bilbo = BilboHouse.cursor()
    MemoryStrategy = """INSERT INTO Chapters(Chapter_Content,UserID,Chapter_Start,Chapter_End)
                         VALUES(%s, %s,%s, %s)"""
    Bilbo.execute(MemoryStrategy,[DatabaseJSON, UserID,ActivityStart,ActivityEnd])
    BilboHouse.commit()
    Frodo = BilboHouse.cursor()
    Frodo.execute("""SELECT Chapter_ID FROM Chapters WHERE Chapter_Content = %s AND UserID = %s""",[DatabaseJSON, UserID])
    return Frodo.fetchall()[0][0]

def InsertChapterTemplate(request,TemplateChapters,TemplateName):
    UserID = Authentication.GetID(request)
    for ChapterID in TemplateChapters:
        Rowling = Connect()
        Potter = Rowling.cursor()
        Potter.execute("INSERT INTO ChapterTemplates(ChapterID, UserID, TemplateName) VALUES(%s,%s,%s)",[ChapterID,UserID,TemplateName])
        Rowling.commit()

def GetiDiaryTemplates(request):
    UserID = Authentication.GetID(request)
    OS = Connect()
    Jobs = OS.cursor()
    Jobs.execute("SELECT ChapterID,TemplateName FROM ChapterTemplates WHERE UserID=%s",[UserID])
    NinetiesMiracles = {}
    for Technology in Jobs.fetchall():
        Microsoft = Connect()
        Gates = Microsoft.cursor()
        Gates.execute("SELECT Chapter_Content FROM Chapters WHERE Chapter_ID=%s",[Technology[0]])
        DOS = Gates.fetchall()
        if Technology[1] not in NinetiesMiracles.keys():
            NinetiesMiracles[Technology[1]]=[[],[]]
            BaseNameForm = re.compile(r'(.*)Q' )
            BaseNameQuest = BaseNameForm.search(Technology[1])
            BasicName = BaseNameQuest.group()
            PublicTemplateName = BasicName[:(len(BasicName)-1)]
            NinetiesMiracles[Technology[1]][0].append(PublicTemplateName)

        NinetiesMiracles[Technology[1]][1].append(DOS[0][0])
    for k,v in NinetiesMiracles.items():
        NinetiesMiracles[k][1] = str(v[1])

    return NinetiesMiracles

def StoriesOfPast(request,FullDate):
    UserID = Authentication.GetID(request)
    Folclor = Connect()
    Erben = Folclor.cursor()
    TailForm = """SELECT Chapter_Content 
                 FROM Chapters
                  WHERE CAST(Chapter_Start AS date) IN ('""" + str(FullDate) + """') AND UserID = %s
                  ORDER BY Chapter_Start"""
    Erben.execute(TailForm,[UserID])
    StoryCollection = Erben.fetchall()
    Flower = []
    for FairyTale in StoryCollection:
        Flower.append(FairyTale[0])
    return Flower

def DeleteDayChapters(request,SubmitFormat):
    UserID = Authentication.GetID(request)
    Lidice = Connect()
    Heidi = Lidice.cursor()
    TailForm = """DELETE FROM Chapters
                  WHERE CAST(Chapter_Start AS date) IN ('""" + SubmitFormat + """') AND UserID = %s"""
    Heidi.execute(TailForm,[UserID])
    Lidice.commit()

def CreateProject(request, Name):
    mydb = Connect()
    mycursor = mydb.cursor()
    BasicName = Name
    token = request.COOKIES["BasicInfo"]
    Name = Name +"€"+str(token)
    Command="""INSERT INTO `RealProjects`(`RealProject_Name`) VALUES (%s)"""
    VariTuple=[Name]
    mycursor. execute(Command,VariTuple)
    mydb.commit()
    Command=("""SELECT RealProject_ID
            FROM RealProjects
            WHERE RealProject_Name = %s""")
    VariTuple=[Name]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    ProjectID = Result[0][0]
    UserID = Authentication.GetID(request)
    Command="""INSERT INTO REL_RealProjects_ActiveUsers(RealProjectID,
    ActiveUserID, RelationType) VALUES (%s,%s,%s)"""
    IDs = [ProjectID,UserID,'Boss']
    mycursor.execute(Command,IDs)
    mydb.commit()
    NewConversaton([UserID],LanguageLoader.LoadWord("GeneralChat","Czech"),ProjectID)
    return ProjectID

def GetProjects(request, ID=""):
    if not ID:
        ID = Authentication.GetID(request)

    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT RealProjectID
            FROM REL_RealProjects_ActiveUsers
            WHERE ActiveUserID= %s """)
    VariTuple=[ID]
    mycursor.execute(Command,VariTuple)
    Result = mycursor.fetchall()
    FinalResult = []
    FullNames = []
    for ToForm in Result:
        Key = ToForm[0]
        Command=("""SELECT RealProject_Name 
                FROM RealProjects
                WHERE RealProject_ID= %s """)
        VariTuple=[Key]
        mycursor.execute(Command,VariTuple)
        Result2 = mycursor.fetchall()[0][0]
        if Result2 not in FullNames:
            FullNames.append(Result2)
            BaseNameForm = re.compile(r'(.*)€' )
            BaseNameQuest = BaseNameForm.search(Result2)
            BasicName = BaseNameQuest.group()
            BasicName = BasicName[:(len(BasicName)-1)]
            ProductPack = {"BasicName":BasicName, "DatabaseName":Result2}
            FinalResult.append(ProductPack)
    return FinalResult

def ProjectVisitorRole(ProjectName, request):
    try:
        UserID = Authentication.GetID(request)
    except KeyError:
        UserRole = "DubiousStranger"
        return UserRole

    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT RelationType
            FROM REL_RealProjects_ActiveUsers
            WHERE RealProjectID= %s AND ActiveUserID =%s""")
    VariTuple=[ProjectID,UserID]
    mycursor.execute(Command,VariTuple)
    Result = mycursor.fetchall()
    Roles = []
    if Result != []:
        Roles = []
        for Role in Result:
            Roles.append(str(Role[0]))
        UserRole = Roles
    else:
        UserRole = "DubiousStranger"
    return UserRole

def ConnectProjectHero(request,HeroName,ProjectName,NotificationRedirect):
    UserID = Authentication.GetID(request)
    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    mycursor = mydb.cursor()
    PartialCommand="""SELECT PassiveUser_ID 
                FROM REL_ActiveUsers_PasiveUsers
                WHERE ActiveUser_ID =""" + str(UserID)
    mycursor.execute(PartialCommand)
    PassiveList = mycursor.fetchall()
    if PassiveList != []:
       SmoothList = str(PassiveList[0][0])
       for ListPart in PassiveList[1:]:
           SmoothList = SmoothList +", " + str(ListPart[0])
       if len(SmoothList)>1:
           MainCommand = """SELECT PasiveUser_ID
                       FROM PasiveUsers
                        WHERE  PasiveUser_Nickname = %s AND
                        PasiveUser_ID IN (""" + SmoothList + """)"""
           VariTuple = [HeroName]
           mycursor.execute(MainCommand,VariTuple)
           Statement = mycursor.statement
           Result = mycursor.fetchall()
       else:
           Result = ""
    else:
        Result = []
    try:
        DerivatedResult = int(Result[0][0])
        TeamInsertor = mydb.cursor()
        INScommand = """INSERT INTO REL_RealProjects_PasiveUsers(RealProjectID, PasiveUserID, RelationType) VALUES (%s,%s,%s)"""
        Values = [ProjectID,DerivatedResult,'TeamMember']
        TeamInsertor.execute(INScommand,Values)
        mydb.commit()
    except IndexError:
        ActiveSelector = mydb.cursor()
        MainCommand = """SELECT ActiveUser_ID
                   FROM ActiveUsers
                    WHERE  CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames) = %s"""
        ActiveSelector.execute(MainCommand,[HeroName])
        ActiveUserID = ActiveSelector.fetchall()[0][0]
        #Send Notification
        BaseNameForm = re.compile(r'(.*)€' )
        BaseNameQuest = BaseNameForm.search(ProjectName)
        BasicName = BaseNameQuest.group()
        BasicName = BasicName[:(len(BasicName)-1)]
        Content = LanguageLoader.LoadWord("ProjectTeamNTF","Czech") + BasicName
        SendNotification(ActiveUserID,Content,BasicName,NotificationRedirect)
        #Create Conversations
        Amalie = mydb.cursor()
        PartyInvitation = """SELECT REL_RealProjects_ActiveUsers.ActiveUserID,
                             CONCAT(ActiveUsers.ActiveUser_FirstName," ", ActiveUsers.ActiveUser_OtherNames)
                             FROM REL_RealProjects_ActiveUsers
                             LEFT JOIN ActiveUsers ON REL_RealProjects_ActiveUsers.ActiveUserID = ActiveUsers.ActiveUser_ID
                             WHERE REL_RealProjects_ActiveUsers.RealProjectID=%s
                            AND (REL_RealProjects_ActiveUsers.RelationType = 'TeamMember'
                           OR REL_RealProjects_ActiveUsers.RelationType = 'Boss')"""
        Amalie.execute(PartyInvitation,[ProjectID])
        Visitors = Amalie.fetchall()
        for VisitorNum,Visitor in enumerate(Visitors):
            NewConversaton([Visitor[0],ActiveUserID],(HeroName+"+"+Visitor[1]),ProjectID=ProjectID,VisitorNum=VisitorNum)

        CreateHeroProjectConnection(ProjectID,ActiveUserID,'TeamMember')

def CreateHeroProjectConnection(ProjectID,ActiveUserID,Role):
    mydb = Connect()
    TeamInsertor = mydb.cursor()
    INScommand = """INSERT INTO REL_RealProjects_ActiveUsers(RealProjectID, ActiveUserID, RelationType) VALUES (%s,%s,%s)"""
    Values = [ProjectID,ActiveUserID,Role]
    TeamInsertor.execute(INScommand,Values)
    mydb.commit()
    GeneralChatKeeper = mydb.cursor()
    GeneralChatCoordinates = """SELECT ID FROM Conversations WHERE RealProjectID = %s AND Name=%s"""
    Coordinates = [ProjectID,LanguageLoader.LoadWord("GeneralChat","Czech")]
    GeneralChatKeeper.execute(GeneralChatCoordinates,Coordinates)
    GeneralChatID = GeneralChatKeeper.fetchall()[0][0]
    ConnectWithConversation(GeneralChatID,ActiveUserID)

def ShowProjectTeam(ProjectName):
    Team = []
    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    mycursor = mydb.cursor()
    #Pasive Users
    Command=("""SELECT PasiveUserID
            FROM REL_RealProjects_PasiveUsers
            WHERE RealProjectID= %s """)
    VariTuple=[ProjectID]
    mycursor.execute(Command,VariTuple)
    Result = mycursor.fetchall()
    mycursor2 = mydb.cursor()
    for ToForm in Result:
        Key = ToForm[0]
        Command=("""SELECT PasiveUser_Nickname 
                FROM PasiveUsers
                WHERE PasiveUser_ID= %s """)
        VariTuple=[Key]
        mycursor2.execute(Command,VariTuple)
        Result2 = (mycursor2.fetchall())[0][0]
        Team.append(Result2)

    #Same things for active
    Command=("""SELECT ActiveUserID
            FROM REL_RealProjects_ActiveUsers
            WHERE RealProjectID= %s """)
    VariTuple=[ProjectID]
    mycursor.execute(Command,VariTuple)
    Result = mycursor.fetchall()
    mycursor2 = mydb.cursor()
    for ToForm in Result:
        Key = ToForm[0]
        Command=("""SELECT CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames) 
                FROM ActiveUsers
                WHERE ActiveUser_ID= %s """)
        VariTuple=[Key]
        mycursor2.execute(Command,VariTuple)
        Result2 = (mycursor2.fetchall())[0][0]
        Team.append(Result2)
    return Team

def CheckProjectBoss(request, ProjectName):
    VisitorRoles = ProjectVisitorRole(ProjectName,request)
    if "{'Boss'}" in VisitorRoles:
        return True
    else:
        return False

def DeleteProject(ProjectName):
    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    BurnoutGuy = mydb.cursor()
    DELcommand = """DELETE FROM RealProjects 
                    WHERE RealProject_ID = %s"""
    BurnoutGuy.execute(DELcommand,[ProjectID])
    mydb.commit()
    return True

def UnconnectProjectHero(Role,ProjectName,HeroName="", HeroID=""):
    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    mycursor = mydb.cursor()
    #Self delete
    if HeroID != "":
        TeamInsertor = mydb.cursor()
        DELcommand = """DELETE FROM REL_RealProjects_ActiveUsers
                        WHERE RealProjectID=%s AND ActiveUserID=%s AND RelationType=%s"""
        Values = [ProjectID,HeroID,Role]
        TeamInsertor.execute(DELcommand,Values)
        mydb.commit()
        return True
    #Delete by Boss
    try:
        PartialCommand="""SELECT PasiveUserID 
                FROM REL_RealProjects_PasiveUsers
                WHERE RealProjectID =""" + str(ProjectID)
        mycursor.execute(PartialCommand)
        PassiveList = mycursor.fetchall()
        SmoothList = str(PassiveList[0][0])
        for ListPart in PassiveList[1:]:
            SmoothList = SmoothList +", " + str(ListPart[0])
        MainCommand = """SELECT PasiveUser_ID
                   FROM PasiveUsers
                    WHERE  PasiveUser_Nickname = %s AND
                    PasiveUser_ID IN (""" + SmoothList + ")"
        VariTuple = [HeroName]
        mycursor.execute(MainCommand,VariTuple)
        Statement = mycursor.statement
        Result = mycursor.fetchall()
        DerivatedResult = int(Result[0][0])
        TeamInsertor = mydb.cursor()
        DELcommand = """DELETE FROM REL_RealProjects_PasiveUsers 
                        WHERE RealProjectID = %s AND PasiveUserID = %s AND RelationType = %s"""
        Values = [int(ProjectID),DerivatedResult,Role]
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
        DELcommand = """DELETE FROM REL_RealProjects_ActiveUsers
                        WHERE RealProjectID=%s AND ActiveUserID=%s AND RelationType=%s"""
        Values = [ProjectID,ActiveUserID,Role]
        TeamInsertor.execute(DELcommand,Values)
        mydb.commit()

def IntroduceTeam(ProjectName,ProductID):
    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    #Pasive team members
    #Pasive Users
    mycursor= mydb.cursor()
    Command=("""SELECT PasiveUserID
            FROM REL_RealProjects_PasiveUsers
            WHERE RealProjectID= %s AND RelationType='TeamMember'""")
    VariTuple=[ProjectID]
    mycursor.execute(Command,VariTuple)
    Result = mycursor.fetchall()
    mycursor2 = mydb.cursor()
    for ToForm in Result:
        Key = ToForm[0]
        Command="""INSERT INTO REL_Projects_PasiveUsers(PasiveUserID,ProjectID,RelationType) 
                VALUES(%s,%s,%s)"""
        VariTuple=[Key, ProductID,'TeamMember']
        mycursor2.execute(Command,VariTuple)
        mydb.commit()
    #Active team members
    Command="""SELECT ActiveUserID
            FROM REL_RealProjects_ActiveUsers
            WHERE RealProjectID= %s AND (RelationType='TeamMember' OR RelationType='Boss')"""
    VariTuple=[ProjectID]
    mycursor.execute(Command,VariTuple)
    Result = mycursor.fetchall()
    mycursor2 = mydb.cursor()
    for ToForm in Result:
        Key = ToForm[0]
        Command="""INSERT INTO REL_Projects_ActiveUsers(ActiveUserID,ProjectID,RelationType) 
                VALUES(%s,%s,%s)"""
        VariTuple=[Key, ProductID,'TeamMember']
        mycursor2.execute(Command,VariTuple)
        mydb.commit()

def CreatProductOfProject(ProjectName,ProductID):
    mydb = Connect()
    ProjectID = GetProjectID(ProjectName)
    TeamInsertor = mydb.cursor()
    INScommand = """INSERT INTO REL_RealProjects_Projects(RealProjectID, ProjectID) VALUES (%s,%s)"""
    Values = [ProjectID,ProductID]
    TeamInsertor.execute(INScommand,Values)
    mydb.commit()

def GetProjectProducts(ProjectName):
    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT ProjectID
            FROM REL_RealProjects_Projects
            WHERE RealProjectID= %s """)
    VariTuple=[ProjectID]
    mycursor. execute(Command,VariTuple)
    Result = mycursor.fetchall()
    FinalResult = []
    FullNames = []
    for ToForm in Result:
        Key = ToForm[0]
        Command=("""SELECT Project_Name 
                FROM Projects
                WHERE Project_ID= %s """)
        VariTuple=[Key]
        mycursor.execute(Command,VariTuple)
        Result2 = mycursor.fetchall()[0][0]
        if Result2 not in FullNames:
            FullNames.append(Result2)
            BaseNameForm = re.compile(r'(.*)ßđ€9@' )
            BaseNameQuest = BaseNameForm.search(Result2)
            BasicName = BaseNameQuest.group()
            BasicName = BasicName[:(len(BasicName)-5)]
            ProductPack = {"BasicName":BasicName, "DatabaseName":Result2}
            FinalResult.append(ProductPack)
    return FinalResult

def CreateProjectComment(request, ProjectName, CommentContent):
    mydb = Connect()
    UserID = Authentication.GetID(request)
    ProjectID = GetProjectID(ProjectName)
    TeamInsertor = mydb.cursor()
    INScommand = """INSERT INTO RealProjectsComments(RPComment_RealProjectID, RPComment_ActiveUserID,RPComment_Content) VALUES (%s,%s,%s)"""
    Values = [ProjectID,UserID,CommentContent]
    TeamInsertor.execute(INScommand,Values)
    mydb.commit()

def GetProjectComments(ProjectName):
    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    mycursor = mydb.cursor()
    PartialCommand="""SELECT RPComment_ActiveUserID, RPComment_Content, CAST(RPComment_BornTime AS CHAR(20)),RPComment_ID
                FROM RealProjectsComments
                WHERE RPComment_RealProjectID =""" + str(ProjectID) + """ ORDER BY RPComment_BornTime DESC"""
                
    mycursor.execute(PartialCommand)
    CommentList = mycursor.fetchall()
    ToSend = []
    for AppendMaterial in CommentList:
        ToSend.append({})
        UpdatedDict=ToSend[(len(ToSend)-1)]
        UpdatedDict["Content"] = AppendMaterial[1]
        UpdatedDict["BornTime"] = AppendMaterial[2]
            #Insert hero
        Samuel = mydb.cursor()
        HeroID = AppendMaterial[0]
        ProphetMission = """SELECT CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames)
                                FROM ActiveUsers
                                WHERE ActiveUser_ID=%s"""
        Samuel.execute(ProphetMission, [HeroID])
        Kings = Samuel.fetchall()
        KingSaul = Kings[0][0]
        UpdatedDict["Speaker"]=KingSaul
        #CollectReactions
        CommentID = AppendMaterial[3]
        mydb = Connect()
        mycursor = mydb.cursor()
        PartialCommand="""SELECT ActiveUserID, Content
                FROM RPCAnswers
                WHERE CommentID =""" + str(CommentID) + """ ORDER BY AnswerTime"""
                
        mycursor.execute(PartialCommand)
        CommentList = mycursor.fetchall()
        Reactions = []
        for Reaction in CommentList:
            Reactions.append({})
            ReactionParameters = Reactions[(len(Reactions)-1)]
            ReactionParameters["Content"] = Reaction[1]
            Samuel = mydb.cursor()
            HeroID = Reaction[0]
            ProphetMission = """SELECT CONCAT(ActiveUser_FirstName," ", ActiveUser_OtherNames)
                                FROM ActiveUsers
                                WHERE ActiveUser_ID=%s"""
            Samuel.execute(ProphetMission, [HeroID])
            Kings = Samuel.fetchall()
            KingSaul = Kings[0][0]
            ReactionParameters["Speaker"]=KingSaul
        UpdatedDict["Reactions"] = Reactions
    #Return
    return ToSend

def GetCommentID(ProjectName,BornTime):
    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    mycursor = mydb.cursor()
    PartialCommand="""SELECT RPComment_ID
                FROM RealProjectsComments
                WHERE RPComment_RealProjectID =%s AND RPComment_BornTime = %s"""
    Values = [ProjectID,BornTime]            
    mycursor.execute(PartialCommand, Values)
    CommentList = mycursor.fetchall()[0][0]
    return CommentList

def AnswerProjectComment(request, ProjectName, Reaction,BornTime):
    UserID = Authentication.GetID(request)
    CommentID = GetCommentID(ProjectName,BornTime)
    Foukalka = Connect()
    Nonsense = Foukalka.cursor()
    AugustinianIdea = """INSERT INTO RPCAnswers(ActiveUserID,CommentID,Content)
                          VALUES(%s,%s,%s)"""
    Nonsense.execute(AugustinianIdea,[UserID,CommentID,Reaction])
    Foukalka.commit()

def GetNotifications(request):
    ID = Authentication.GetID(request)
    mydb = Connect()
    mycursor = mydb.cursor()
    Command=("""SELECT Head,Content,Sawn, ID,Redirect
            FROM Notifications
            WHERE ActiveUserID= %s 
            ORDER BY SendingTime DESC""")
    VariTuple=[ID]
    mycursor.execute(Command,VariTuple)
    Result = mycursor.fetchall()
    AllNotifications = []
    for ToForm in Result:
        AllNotifications.append({})
        NotificationParameters = AllNotifications[(len(AllNotifications)-1)]
        NotificationParameters["Head"] = ToForm[0]
        NotificationParameters["Content"] = ToForm[1]
        NotificationParameters["Sawn"] = ToForm[2]
        NotificationParameters["ID"] = ToForm[3]
        NotificationParameters["Redirect"] = ToForm[4]

    return AllNotifications

def SendNotification(ActiveUserID,Content,Head,Redirect):
    Facebook = Connect()
    Medved = Facebook.cursor()
    COMMAND ="""INSERT INTO Notifications(ActiveUserID,Content,Head,Redirect) VALUES(%s,%s,%s,%s)"""
    Values = [ActiveUserID,Content,Head,Redirect]
    Medved.execute(COMMAND,Values)
    Facebook.commit()

def DeleteNotification(request,ID):
    UserID = Authentication.GetID(request)
    GrimPlace = Connect()
    Robspiere = GrimPlace.cursor()
    Verdict = "DELETE FROM Notifications WHERE ActiveUserID = %s AND ID= %s"
    Sins = [UserID, ID]
    Robspiere.execute(Verdict,Sins)
    GrimPlace.commit()

def ReadNotification(request,ID):
    UserID = Authentication.GetID(request)
    GrimPlace = Connect()
    Robspiere = GrimPlace.cursor()
    Verdict = "UPDATE Notifications SET Sawn=1 WHERE ActiveUserID = %s AND ID= %s"
    Sins = [UserID, ID]
    Robspiere.execute(Verdict,Sins)
    GrimPlace.commit()

def NewConversaton(Users,Name,ProjectID="",VisitorNum=""):
    mydb = Connect()
    SocialInsertor = mydb.cursor()
    INScommand = """INSERT INTO Conversations(ID,Name, RealProjectID) VALUES (%s,%s,%s)"""
    ID = int(str(VisitorNum)+str(round(time.time())))
    Values = [ID,Name,ProjectID]
    SocialInsertor.execute(INScommand,Values)
    mydb.commit()
    for User in Users:
        ConnectWithConversation(ID,User)

def GetProjectConversations(ProjectName,request):
    UserID = Authentication.GetID(request)
    ProjectID = GetProjectID(ProjectName)
    mydb = Connect()
    mycursor = mydb.cursor()
    PartialCommand="""SELECT Conversations.Name, Conversations.ID
                FROM REL_ActiveUsers_Conversations
                LEFT JOIN Conversations ON REL_ActiveUsers_Conversations.ConversationID = Conversations.ID 
                WHERE Conversations.RealProjectID = %s AND REL_ActiveUsers_Conversations.UserID = %s"""
    mycursor.execute(PartialCommand,[ProjectID,UserID])
    ConversationList = mycursor.fetchall()
    Conversations = []
    for Conversation in ConversationList:
        Conversations.append({})
        UpdatedDict = Conversations[len(Conversations)-1]
        UpdatedDict["Name"] = Conversation[0]
        UpdatedDict["ID"] = Conversation[1]
        UpdatedDict["NewCount"] = UnreadChatsCount(Conversation[1],UserID)
        MessageCollector = mydb.cursor()
        MissionMotto = """SELECT RealProjectsChats.Content,
                             CONCAT(ActiveUsers.ActiveUser_FirstName," ", ActiveUsers.ActiveUser_OtherNames), CAST(RealProjectsChats.BornTime AS CHAR(20))
                             FROM RealProjectsChats
                             LEFT JOIN ActiveUsers ON RealProjectsChats.AuthorID = ActiveUsers.ActiveUser_ID
                             WHERE RealProjectsChats.ConversationID=%s
                             ORDER BY RealProjectsChats.BornTime"""
        MessageCollector.execute(MissionMotto,[Conversation[1]])
        Posts = MessageCollector.fetchall()
        UpdatedDict["Posts"] = Posts
        try:
            UpdatedDict["Actuality"] = Posts[len(Posts)-1][2]
        except IndexError:
            pass
    return Conversations

def AddChatMessage(request, ConversationID, Content):
    UserID = Authentication.GetID(request)
    Foukalka = Connect()
    Nonsense = Foukalka.cursor()
    AugustinianIdea = """INSERT INTO RealProjectsChats(AuthorID, Content, ConversationID)
                          VALUES(%s,%s,%s)"""
    Nonsense.execute(AugustinianIdea,[UserID,Content,ConversationID])
    Foukalka.commit()

def LoadChat( ConversationID, LastTime):
    mydb=Connect()
    MessageCollector = mydb.cursor()
    MissionMotto = """SELECT RealProjectsChats.Content,
                             CONCAT(ActiveUsers.ActiveUser_FirstName," ", ActiveUsers.ActiveUser_OtherNames), CAST(RealProjectsChats.BornTime AS CHAR(20))
                             FROM RealProjectsChats
                             LEFT JOIN ActiveUsers ON RealProjectsChats.AuthorID = ActiveUsers.ActiveUser_ID
                             WHERE RealProjectsChats.ConversationID=%s AND RealProjectsChats.BornTime > %s
                             ORDER BY RealProjectsChats.BornTime"""
    MessageCollector.execute(MissionMotto,[ConversationID, LastTime])
    Posts = MessageCollector.fetchall()
    return Posts

def ConnectWithConversation(ConversationID,UserID):
    mydb = Connect()
    PeopleConecter = mydb.cursor()
    Invitation = """INSERT INTO REL_ActiveUsers_Conversations(ConversationID,UserID) VALUES (%s,%s)"""
    Values = [ConversationID,UserID]
    PeopleConecter.execute(Invitation,Values)
    mydb.commit()

def UnreadChatsCount(ConversationID,UserID):
    mydb = Connect()
    MessageCollector = mydb.cursor()
    MissionMotto = """SELECT COUNT(RealProjectsChats.ID)
                             FROM RealProjectsChats
                             LEFT JOIN REL_ActiveUsers_Conversations ON REL_ActiveUsers_Conversations.ConversationID = RealProjectsChats.ConversationID
                             WHERE RealProjectsChats.ConversationID=%s
                            AND REL_ActiveUsers_Conversations.LastChecked < RealProjectsChats.BornTime
                           AND REL_ActiveUsers_Conversations.UserID = %s """
    MessageCollector.execute(MissionMotto,[ConversationID,UserID])
    Postcount = MessageCollector.fetchall()
    return Postcount[0][0]

def UpdateConersationLastLook(ConversationID,request):
    UserID = Authentication.GetID(request)
    GrimPlace = Connect()
    Robspiere = GrimPlace.cursor()
    Verdict = "UPDATE REL_ActiveUsers_Conversations SET LastChecked = %s WHERE UserID = %s AND ConversationID= %s"
    Sins = [datetime.datetime.fromtimestamp(time.time()),UserID, ConversationID]
    Robspiere.execute(Verdict,Sins)
    GrimPlace.commit()