from django.db import models

# Create your models here.
class contactus(models.Model):
    mail = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    description = models.CharField(max_length=500)

class admincontact(models.Model):
    mail = models.CharField(max_length=200)
    resume = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200)
    github = models.CharField(max_length=200)
    linkedin = models.CharField(max_length=200)
    leetcode = models.CharField(max_length=200)
    hackerrank = models.CharField(max_length=200)