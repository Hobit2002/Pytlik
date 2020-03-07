from django.shortcuts import render,redirect
from django.template import RequestContext
import json, re,time,sys,os
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Dataseer'))
import Authentication,LanguageLoader

#1.
def gate(request):
    return redirect("Home")
    #1.1.Direct user on appropriate page



