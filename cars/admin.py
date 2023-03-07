from django.contrib import admin

# Register your models here.
from cars.models import Car,Car_Images
admin.site.register(Car)
admin.site.register(Car_Images)
