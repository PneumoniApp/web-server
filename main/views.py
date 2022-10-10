from cgitb import text
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
import os
from django.conf import settings
from django.template.loader import render_to_string
import pandas as pd
import numpy as np
# Create your views here.


def home(response):
    if response.user.is_authenticated:
        username=response.user.username
        return render(response,"main/home.html",{"username":username})
    return redirect("/")
    
def initial(response):
    return render(response,"main/initial.html",{})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n= form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response,"main/create.html",{"form":form})



def information(response):
    if response.user.is_authenticated:
        username=response.user.username
        data = pd.read_csv("/var/www/web-server/metrics.csv")
        x=data['accuracy'].tolist()
        x2=data['loss'].tolist()
        x3=data['val_loss'].tolist()
        x4=data['val_accuracy'].tolist()
        y=list(np.arange(500))
        return render(response,"main/information.html",{"username":username,"x":x,"y":y,"x2":x2,"x3":x3,"x4":x4})
    return redirect("/")
