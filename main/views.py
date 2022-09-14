from cgitb import text
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import ToDoList,Item
from .forms import CreateNewList
import requests
import os
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.

def index(response,id):
    ls=ToDoList.objects.get(id=id)
    #item = ls.item_set.get(id=1)
    #return HttpResponse("<h1>%s</h1><br></br><p>%s</p>" %( ls.name,str(item.text)))

    if ls in response.user.todolist.all():

        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c"+ str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete= False

                    item.save()
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt)>2:
                    ls.item_set.create(text=txt, complete= False)
                else:
                    print("invalid")
        return render(response,"main/list.html",{"ls":ls})    
    return render(response,"main/view.html",{})   

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

def view(response):
    return render(response, "main/view.html",{})


def information(response):
    if response.user.is_authenticated:
        username=response.user.username
        return render(response,"main/information.html",{"username":username})
    return redirect("/")