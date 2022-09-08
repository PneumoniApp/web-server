from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from .forms import RegisterForm

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            print("The form is valid")
            form.save()    
            return redirect("/home")
        return render(response, "register/register.html", {"form":form})
    form = RegisterForm()
    return render(response, "register/register.html", {"form":form})