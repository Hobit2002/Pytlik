import time, sys, os
import mysql.connector
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Database

mydb = Database.Connect()
while True:
	YoungCleaner = mydb.cursor()
	YoungCleaner.execute("""DELETE FROM Session WHERE Session_EventTime < DATEADD(month, 2, CreateDate) < DATEADD( mi,-15,GETDATE())""")