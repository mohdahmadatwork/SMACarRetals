from django.db import models
from cars.models import Car
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Order(models.Model):
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    tennant = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    tennant_address = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField()
    dl = models.ImageField(upload_to="DL/images/")
    book_date = models.DateTimeField(default=timezone.now)
    return_b = models.BooleanField(default=False)
    late_b = models.BooleanField(default=False)
    return_date = models.DateTimeField(blank=True,null=True,default=None)
    price = models.IntegerField(default=0)
    late_charge = models.IntegerField(default=0)
    cancel_charge = models.IntegerField(default=0)
    price_per_day= models.IntegerField(default=0)
    cancel_b = models.BooleanField(default=False)

class CancelOrder(models.Model):
    order =  models.ForeignKey(Order,on_delete=models.CASCADE)
    cancel_date = models.DateTimeField(auto_now_add=True)
