from django.shortcuts import render,redirect
from home.models import contactus,admincontact
from django.contrib import messages 

# Create your views here.
def home(request):
    return render(request,"home.html")

def about(request):
    developer =  admincontact.objects.get()
    return render(request,"about.html",{"developer":developer})

def contactusf(request):
    developer =  admincontact.objects.get()
    if request.method=="POST":
        mail = request.POST["email"]
        name = request.POST["name"]
        address = request.POST["address"]
        description = request.POST["description"]
        contactForm = contactus()
        contactForm.mail = mail
        contactForm.name = name
        contactForm.address = address
        contactForm.description = description
        contactForm.save()
        messages.success(request,"We will be back to you!")
        return redirect("/contactus")
    return render(request,"contactus.html",{"developer":developer})