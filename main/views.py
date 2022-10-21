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
# send email
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
#

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

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'pneumoniapp.tech',
					'site_name': 'pneumoniapp',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'dontreply@pneumoniapp.tech' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})