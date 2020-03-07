from pathlib import Path
import os

def ShowInConsole(ToWrite):
    ToWrite = '\n' + str(ToWrite)
    InnerText = open('Dataseer\console.txt','a')
    InnerText.write(ToWrite)
    InnerText.close()
