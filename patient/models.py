from django.db import models
from django.contrib.auth.models import User
class Patient(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="patient",null=True)
    name= models.CharField(max_length=200)
    sex = models.BooleanField(default=0)
    age = models.IntegerField(default=0)
    weight = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    nss = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

