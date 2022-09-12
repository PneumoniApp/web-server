from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
class CreateNewPatient(forms.Form):
    name= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Patient name',"class":"form-control mb-3"}), label="Name",max_length=200)
    CHOICES = [('0', 'Male'), ('1', 'Female')]
    sex= forms.ChoiceField(widget=forms.RadioSelect(attrs={"type":"radio"}), choices=CHOICES, label="Sex")
    age= forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',"type":"number","min":0,"max":110}), label="Age")
    weight= forms.FloatField(label="Weight on kg", validators=[MaxValueValidator(limit_value=635,message="max value = 635"),MinValueValidator(limit_value=0,message="min value = 0")] ,widget=forms.NumberInput(attrs={'class': 'form-control',"type":"number","min":0,"max":635}))
    height= forms.FloatField(label="Height on cm", validators=[MaxValueValidator(limit_value=251,message="max value = 251"),MinValueValidator(limit_value=0,message="min value = 0")],widget=forms.NumberInput(attrs={'class': 'form-control',"type":"number","min":0,"max":251}))
    nss = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Patient internal id',"class":"form-control mb-3"}), label="NSS",max_length=200,required=False)

