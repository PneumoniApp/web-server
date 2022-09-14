from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import XRay, Comment
from .forms import CreateNewXRay , CreateNewComment
from patient.models import Patient
import requests
import os
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.

def createPrediction(response):
    patient=Patient.objects.filter(user_id=response.user.id)
    ch= [(p.id,str(p.nss)+" ("+str(p.name)+ ")") for p in patient]
    if response.method == "POST":
        form = CreateNewXRay(response.POST,response.FILES,choice=ch)

        if form.is_valid():
            n= form.cleaned_data["patient"]
            i= form.cleaned_data.get("img")
            x = XRay(patient_id=n, img=i)
            x.save()
            response.user.xray.add(x)
            patient=Patient.objects.get(id=x.patient_id)
            form = CreateNewComment()
            com=Comment.objects.filter(xray_id=x.id)
            return render(response,"prediction/nonLoadPrediction.html",{"xray":x,"patient":patient,"form":form,"comments":com})
    else:
        form = CreateNewXRay(choice=ch)
       
    return render(response,"prediction/create.html",{"form":form})

def viewPrediction(response,id):
    if response.method == "POST":
        form = CreateNewComment(response.POST)

        if form.is_valid():
            t= form.cleaned_data["text"]
            c = Comment(text=t, xray_id=id)
            c.save()
        return HttpResponseRedirect("/viewPrediction/%i" %id)
    else:        
        form = CreateNewComment()
    x=XRay.objects.get(id=id)
    patient=Patient.objects.get(id=x.patient_id)
    result=["Normal", "Pneumonia"]
    com=Comment.objects.filter(xray_id=x.id)
    return render(response, "prediction/viewPrediction.html",{"xray":x,"result":result[x.result],"patient":patient,"form":form,"comments":com})

def indexPrediction(response):
    xray=XRay.objects.filter(user_id=response.user.id)
    names=[]
    for i in xray:
        names.append(Patient.objects.get(id=i.patient_id).name)
    ls=zip(xray,names)
    return render(response,"prediction/indexPrediction.html",{"ls":ls})   


def deleteXray(response,id):
    x=XRay.objects.get(id=id)
    x.delete()
    return redirect("/home/")

def deleteComment(response,id,xray_id):
    c=Comment.objects.get(id=id)
    c.delete()
    return redirect("/viewPrediction/"+str(xray_id))

def process_data_xray(response):
    file_path = os.path.join(settings.MEDIA_ROOT, 'cat.jpg')
    resp = requests.post("http://localhost:5000/predict",
                    files={"file": open(file_path,'rb')})
    context=resp.json()
    
    result=render_to_string("prediction/load_result.html",context)
    
    chart=render_to_string("prediction/load_chart.html",context)
    
    data = {'result': result,'chart':chart}
    return JsonResponse(data)