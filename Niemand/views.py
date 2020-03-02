from django.shortcuts import render
from django.template import RequestContext
import json, re,time
from pathlib import Path


#1.
def gate(request):
    #1.1.Direct user on appropriate page
    try:
        #1.1. -a) If user is logged in, direct him on his profile.
        User = request.COOKIES["token"]

    
    except:
        #1.1. - b) If you can´t recognize any user, direct visitor on home page
        #1.1.2. - b) Get content of page
        ReadIt = Path('languages\Pages.txt')
        InnerText = ReadIt.read_text()
        Pages =json.loads(InnerText)
        PageContent = Pages["AboutUs"]
        #1.1.3. -b) And translate it into language of page
        #1.1.3.1 -b)Load dictionary
        ReadIt = Path('languages\Dictionary.txt')
        InnerText = ReadIt.read_text()
        Dictionary =json.loads(InnerText)
        #1.1.3.2 - b)Choose right language
        Language = "Czech"
        Language = Dictionary[Language]
        #1.1.3.3. -b) Finally translate
        LanguagePack = {}
        for ToTranslate in PageContent:
            LanguagePack[ToTranslate] = Language[ToTranslate]
        return render(request,"Niemand\AboutUs.html", LanguagePack)


