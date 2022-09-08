from django import forms

class CreateNewXRay(forms.Form):
    name= forms.CharField(label="Name",max_length=200)
    img= forms.ImageField(label="Xray image")