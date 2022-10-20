from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Patient
from .forms import CreateNewPatient
from prediction.models import XRay
# Create your views here.

def createPatient(response):
    if response.method == "POST":
        form = CreateNewPatient(response.POST)

        if form.is_valid():
            n= form.cleaned_data["name"]
            s= form.cleaned_data.get("sex")
            a=form.cleaned_data.get("age")
            w=form.cleaned_data.get("weight")
            h=form.cleaned_data.get("height")
            n_ss=form.cleaned_data.get("nss")
            x = Patient(name=n,sex=s,age=a,weight=w,height=h,nss=n_ss)
            x.save()
            response.user.patient.add(x)
        return HttpResponseRedirect("/viewPatient/%i" %x.id)
    else:
        form = CreateNewPatient()
    return render(response,"patient/create.html",{"form":form})

def editPatient(response,id):
    if response.method == "POST":
        form = CreateNewPatient(response.POST)

        if form.is_valid():
            n= form.cleaned_data["name"]
            s= form.cleaned_data.get("sex")
            a=form.cleaned_data.get("age")
            w=form.cleaned_data.get("weight")
            h=form.cleaned_data.get("height")
            n_ss=form.cleaned_data.get("nss")
            x=Patient.objects.get(id=id)
            x.name=n
            x.sex=s
            x.age=a
            x.weight=w
            x.height=h
            x.nss=n_ss
            x.save()
        return HttpResponseRedirect("/viewPatient/%i" %x.id)
    else:
        x=Patient.objects.get(id=id)
        form = CreateNewPatient(initial={'name':x.name,'sex':x.sex,'age':x.age,'weight':x.weight,'height':x.height,'nss':x.nss})
    return render(response,"patient/edit.html",{"form":form})

def viewPatient(response,id):
    x=Patient.objects.get(id=id)
    ls=XRay.objects.filter(patient_id=id)
    return render(response, "patient/viewPatient.html",{"patient":x, "ls":ls})

def indexPatient(response):
    ls=Patient.objects.filter(user_id=response.user.id)
    return render(response,"patient/indexPatient.html",{"ls":ls})   

def deletePatient(response,id):
    x=Patient.objects.get(id=id)
    x.delete()
    return redirect("/home/")