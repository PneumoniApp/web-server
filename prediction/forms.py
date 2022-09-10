from django import forms
class CreateNewXRay(forms.Form):
    name= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Patient name',"class":"form-control mb-3"}), label="Name",max_length=200)
    img= forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control mb-3"}), label="Xray image")