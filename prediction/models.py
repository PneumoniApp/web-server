from django.db import models
from django.contrib.auth.models import User
from  django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from uuid import uuid4
from patient.models import Patient
def path_and_rename(path):
        def wrapper(instance, filename):
            ext = filename.split('.')[-1]
            # get filename
            if instance.pk:
                filename = '{}.{}'.format(instance.pk, ext)
            else:
                # set filename as random string
                filename = '{}.{}'.format(uuid4().hex, ext)
            # return the whole path to the file
            return os.path.join(path, filename)
        return wrapper
# Create your models here.
class XRay(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="xray",null=True)
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient")
    img= models.ImageField(upload_to =path_and_rename("xray_images/"))
    result = models.BooleanField(default=0)
    normal_level = models.FloatField(default=0.0)
    pneumonia_level = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

@receiver(post_delete, sender=XRay)
def post_delete_image(sender, instance, *args, **kwargs):
    try:
        instance.img.delete(save=False)#delete image from filesystem
    except:
        pass
    try:
        #Here delete img from bck database
        bck=XRayBck.objects.using('pneumonia_bck').get(id=instance.id)
        bck.delete()
    except:
        pass

class Comment(models.Model):
    xray=models.ForeignKey(XRay,on_delete=models.CASCADE)
    text = models.CharField(max_length=600)
    date= models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.text

class XRayBck(models.Model):
    img= models.BinaryField()
    
    def __str__(self):
        return "image"