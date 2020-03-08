import mysql.connector
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Consolewriter

def Connect():
    mydb = mysql.connector.connect(
    host="bejt.local",
    user="pytlikapp",
    passwd="Trochu-KRATS-190",
    database="pytlik",
    port ="3307")
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
    Consolewriter.ShowInConsole(DataPack)
    mycursor2.execute(Command,DataPack)
    mydb.commit()