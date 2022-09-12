from secrets import choice
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import XRay
from .forms import CreateNewXRay
from patient.models import Patient
# Create your views here.

def createPrediction(response):
    patient=Patient.objects.filter(user_id=response.user.id)
    ch= [(p.id,p.name) for p in patient]
    if response.method == "POST":
        form = CreateNewXRay(response.POST,response.FILES,choice=ch)

        if form.is_valid():
            n= form.cleaned_data["patient"]
            i= form.cleaned_data.get("img")
            x = XRay(patient_id=n, img=i)
            x.save()
            response.user.xray.add(x)
            return HttpResponseRedirect("/viewPrediction/%i" %x.id)
    else:
        form = CreateNewXRay(choice=ch)
       
    return render(response,"prediction/create.html",{"form":form})

def viewPrediction(response,id):
    x=XRay.objects.get(id=id)
    patient=Patient.objects.get(id=x.patient_id)
    result=["Normal", "Pneumonia"]
    return render(response, "prediction/viewPrediction.html",{"xray":x,"result":result[x.result],"patient":patient})

def indexPrediction(response):
    ls=XRay.objects.filter(user_id=response.user.id)
    return render(response,"prediction/indexPrediction.html",{"ls":ls})   