from django.db import models
from django.contrib.auth.models import User
import os
from uuid import uuid4
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
    name= models.CharField(max_length=200)
    img= models.ImageField(upload_to =path_and_rename("xray_images/"))
    result = models.BooleanField(default=0)
    normal_level = models.FloatField(default=0.0)
    pneumonia_level = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Comment(models.Model):
    xray=models.ForeignKey(XRay,on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    date= models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.text
