from django import forms
from patient.models import Patient
from django.contrib.auth.models import User
class CreateNewXRay(forms.Form):
    #choice=[]
    #patient= None
    #img= forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control mb-3"}), label="Xray image")
    def __init__(self, *args, **kwargs):
        ch=kwargs.pop('choice',[])
        super(CreateNewXRay, self).__init__(*args, **kwargs)
        self.fields['patient']=forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control mb-3"}) ,choices=ch, label="Patient")
        self.fields['img']= forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control mb-3 "}), label="Xray image")