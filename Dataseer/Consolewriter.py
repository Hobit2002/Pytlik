from pathlib import Path
import os

def sic(ToWrite):
    ToWrite = '\n' + str(ToWrite)
    InnerText = open('Dataseer\console.txt','a')
    InnerText.write(ToWrite)
    InnerText.close()
