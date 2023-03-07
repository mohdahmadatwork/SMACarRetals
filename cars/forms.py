from django import forms
from cars.models import Car_Images,Car

class CarImagesForm(forms.ModelForm):
    foreign_key = forms.ModelChoiceField(queryset=Car.objects.all())
    print(foreign_key)
    # def __init__(foreign_key):
    class Meta:
        model = Car_Images
        fields = ["images","car"]