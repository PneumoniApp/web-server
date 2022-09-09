from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import XRay
from .forms import CreateNewXRay
# Create your views here.

def createPrediction(response):
    if response.method == "POST":
        form = CreateNewXRay(response.POST,response.FILES)

        if form.is_valid():
            n= form.cleaned_data["name"]
            i= form.cleaned_data.get("img")
            print(i)
            x = XRay(name=n, img=i)
            x.save()
            response.user.xray.add(x)
        return HttpResponseRedirect("/viewPrediction/%i" %x.id)
    else:
        form = CreateNewXRay()
    return render(response,"prediction/create.html",{"form":form})

def viewPrediction(response,id):
    x=XRay.objects.get(id=id)
    result=["Normal", "Pneumonia"]
    return render(response, "prediction/viewPrediction.html",{"xray":x,"result":result[x.result]})
    #return HttpResponse("Here is going to show the results: id=%i" %id)