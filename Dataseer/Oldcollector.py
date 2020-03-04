import time, sys, os
import mysql.connector
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Database

mydb = Database.Connect()
def commit(mydb):
    mydb.commit()
    
def execute(mydb):
    YoungCleaner = mydb.cursor()
    YoungCleaner.execute("""DELETE FROM Session WHERE DATE_ADD(NOW(), INTERVAL 1 SECOND)""")
    commit(mydb)
    
while True:
    execute(mydb)
    
