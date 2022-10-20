from traceback import print_tb
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import XRay, Comment, XRayBck
from .forms import CreateNewXRay , CreateNewComment
from patient.models import Patient
import requests
import os
from django.conf import settings
from django.template.loader import render_to_string
import base64
from django.core.files.base import ContentFile
from django.core.files import File
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
            #bck of image binary field
            path=str(x.img.path)
            image_bck=open(path,'rb')
            image_read=image_bck.read()
            bck= XRayBck(img=image_read)
            bck.pk=x.pk
            bck.save(using='pneumonia_bck')
            form = CreateNewComment()
            com=Comment.objects.filter(xray_id=x.id)
            return render(response,"prediction/nonLoadPrediction.html",{"xray":x,"patient":patient,"form":form,"comments":com})
    else:
        form = CreateNewXRay(choice=ch)
       
    return render(response,"prediction/create.html",{"form":form})

def createSpecificPrediction(response,id):
    patient=Patient.objects.filter(user_id=response.user.id)
    sp=patient.filter(id=id)
    ch= [(p.id,str(p.nss)+" ("+str(p.name)+ ")") for p in sp]
    if response.method == "POST":
        form = CreateNewXRay(response.POST,response.FILES,choice=ch)

        if form.is_valid():
            n= form.cleaned_data["patient"]
            i= form.cleaned_data.get("img")
            x = XRay(patient_id=n, img=i)
            x.save()
            response.user.xray.add(x)
            patient=Patient.objects.get(id=x.patient_id)
            #bck of image binary field
            path=str(x.img.path)
            image_bck=open(path,'rb')
            image_read=image_bck.read()
            bck= XRayBck(img=image_read)
            bck.pk=x.pk
            bck.save(using='pneumonia_bck')
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
    path=str(x.img.path)
    if not os.path.exists(path):
        retrieve_from_bck_db(x)
    patient=Patient.objects.get(id=x.patient_id)
    result=["Normal", "Pneumonia"]
    com=Comment.objects.filter(xray_id=x.id)
    return render(response, "prediction/viewPrediction.html",{"xray":x,"result":result[x.result],"patient":patient,"form":form,"comments":com})

def retrieve_from_bck_db(xray):
    #print("El archivo no se encontro... Recuperando de bck db")
    bck=XRayBck.objects.using('pneumonia_bck').get(id=xray.id)
    path=str(xray.img.path)
    data = bck.img
    with open(path,'wb') as f:
        file=File(f)
        file.write(data)
    #print("SE recupero la imagen")


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

def process_data_xray(response,id):
    x=XRay.objects.get(id=id)
    path=str(x.img.path)
    try:
        resp = requests.post("http://ia.pneumoniapp.tech/predict",
                    files={"file": open(path,'rb')})
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        data = {'result': "Error:invalid http response",'chart':str(err)}
        return JsonResponse(data)
    except requests.exceptions.Timeout:
        data = {'result': "Error:timeout",'chart':"Error:timeout"}
        return JsonResponse(data)
    except requests.exceptions.ConnectionError:
        data = {'result': "Error:Connection Error",'chart':"Error:Connection Error"}
        return JsonResponse(data)
    context=resp.json()
    context=resp.json()
    result=render_to_string("prediction/load_result.html",context)
    chart=render_to_string("prediction/load_chart.html",context)
    data = {'result': result,'chart':chart}
    x.result=context['result']
    x.normal_level=context['ps1']
    x.pneumonia_level=context['ps2']
    x.save()
    return JsonResponse(data)
    
