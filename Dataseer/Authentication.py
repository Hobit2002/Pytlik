import time
import mysql.connector
import ip

def Authenticate(request,UserID):
    token = UserID
    mydb = mysql.connector.connect(
    host="bejt.local",
    user="pytlikapp",
    passwd="Trochu-KRATS-190",
    database="pytlik",
    port ="3307")
    mycursor2 = mydb.cursor()
    IP = ip.visitor_ip_address(request)
    Command=("""INSERT INTO `Session`( Session_UserID, Session_UserToken, Session_UserDevice)
    VALUES (%s,%s,%s)""")
    VariTuple=(UserID,token,IP)
    mycursor2.execute(Command,VariTuple)
    mydb.commit()
    return token

def CheckUser(IP,token):
    return True