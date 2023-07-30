from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.
class Client_images(models.Model):
    images = models.ImageField(upload_to='Client/image')
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email_token = models.CharField(max_length=2000)
    is_verified = models.BooleanField(default=False)
    
class tennantaddress(models.Model):
    tennant = models.ForeignKey(User,on_delete=models.CASCADE)
    tennant_address = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField()
    dl = models.ImageField(upload_to="DL/images/")