from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Car(models.Model):
    car_number = models.CharField(max_length=25)
    company = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    rent_price = models.IntegerField()
    availablity = models.BooleanField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=42)
    description = models.TextField(default="")
    fine = models.IntegerField(default=0)
    cancel_charge = models.IntegerField(default=0)

class Car_Images(models.Model):
    images = models.ImageField(upload_to="cars/images")
    car = models.ForeignKey(Car,related_name='images',on_delete=models.CASCADE)
    