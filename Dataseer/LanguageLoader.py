import json, re,time,sys,os, time
from pathlib import Path

def Language(PageName,Language):
    InnerText = open('languages\pages.json','r')

    Pages = json.load(InnerText)
    PageContent = Pages[PageName]
    #1.1.3. -b) And translate it into language of page
    #1.1.3.1 -b)Load dictionary
    InnerText= open('languages\dictionary2.json','r')
    Dictionary =json.load(InnerText)
    #1.1.3.2 - b)Choose right language
    Language = Dictionary[Language]
    #1.1.3.3. -b) Finally translate
    LanguagePack = {}
    for ToTranslate in PageContent:
        LanguagePack[ToTranslate] = Language[ToTranslate]
    return LanguagePack

def LoadWord(Word, Language):
    #1.1.3. -b) And translate it into language of page
    #1.1.3.1 -b)Load dictionary
    InnerText= open('languages\dictionary2.json','r')
    Dictionary =json.load(InnerText)
    #1.1.3.2 - b)Choose right language
    Language = Dictionary[Language]
    Translated = Language[Word]
    return Translated

def GetKeys(Values,Language):
    InnerText= open('languages\dictionary2.json','r')
    Dictionary =json.load(InnerText)[Language]
    TransformedDictionary = {}
    for k,v in Dictionary.items():
        TransformedDictionary[v] = k
    Keys = []
    for q in Values:
        Keys.append(TransformedDictionary[q])
    return Keys

def AddToDictionary(Language,Key,Value):
    InnerText= open('languages\dictionary2.json','r')
    Dictionary =json.load(InnerText)
    Dictionary[Language][Key] = Value
    ToSave = json.dumps(Dictionary)
    DataFile = open('languages\dictionary2.json', 'w')
    DataFile.write(ToSave)
    DataFile.close()