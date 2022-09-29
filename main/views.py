from cgitb import text
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
import os
from django.conf import settings
from django.template.loader import render_to_string
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
        return render(response,"main/information.html",{"username":username})
    return redirect("/")
