import json, re,time,sys,os, time
from pathlib import Path

def Language(PageName,Language):
    InnerText = open('languages\pages2.json','r')

    Pages = json.load(InnerText)
    PageContent = Pages[PageName]
    #1.1.3. -b) And translate it into language of page
    #1.1.3.1 -b)Load dictionary
    InnerText= open('languages\Dictionary.json','r')
    Dictionary =json.load(InnerText)
    #1.1.3.2 - b)Choose right language
    Language = Dictionary[Language]
    #1.1.3.3. -b) Finally translate
    LanguagePack = {}
    for ToTranslate in PageContent:
        LanguagePack[ToTranslate] = Language[ToTranslate]
    return LanguagePack