from django.shortcuts import render,redirect
from cars.models import Car,Car_Images
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib import messages
from cars.forms import CarImagesForm
from client.models import tennantaddress
# Create your views here.
def available_cars(request):
    if not request.user.is_authenticated:
        cars = Car.objects.filter(availablity = True)
        return render(request,'availablecars.html',{"cars":cars})
    else:
        user = request.user
        group = user.groups.all().get()
        groupname = group.name
        if groupname == "client":
            cars = Car.objects.filter(availablity = True)
            return render(request,'availablecars.html',{"cars":cars,"groupname":groupname})
        else:
            cars = Car.objects.filter(owner=request.user)
            return render(request,'availablecars.html',{"cars":cars,"groupname":groupname})

            

def car_detail(request,str):
    car = Car.objects.get(pk=str)
    return render(request,"detailcar.html",{"car":car})

def add_car(request):
    if request.method=="POST":
        user = request.user
        # print(user)
        usergroup = user.groups.all()
        # print(usergroup)
        group=usergroup.get()
        # print(group)
        if group.name == 'owner':
            car_number = request.POST["car_number"]
            company = request.POST["company"]
            model = request.POST["model"]
            rent_price = request.POST["rent_price"]
            noofimage=request.POST["noofimage"]
            noofimage = int(noofimage)
            # print(type(noofimage))
            car=Car (car_number=car_number,company=company,model=model,rent_price=rent_price,availablity=True,owner=request.user)
            car.save()
            return render(request,"addcarimages.html",{"no_of_image":range(int(noofimage)),"carid":car.id,"noofimage":str(noofimage)})
        else:
            return redirect("/")
    else:
        user = request.user
        add = tennantaddress.objects.filter(tennant=user).get()
        return render(request,"addcar.html",{"add":add})      

def add_car_images(request,id):
    if request.method=="POST":
        
        noofimage = request.POST["noofimage"]
        car = Car.objects.get(pk=id)
        if(car.images.all().count()>0):
            car.images.all().delete()
        for i in range(int(noofimage)):
            carimages = Car_Images()
            name="carimage"+str(i)
            print(name)
            if(len(request.FILES[name])!=0):
                carimages.images=request.FILES[name]
                carimages.car=car
                carimages.save()
        messages.success(request,"Car with model name "+car.model+" added successfully")
        return redirect("/")
    else:
        return render(request,"addcarimages")



def delete_car(request,id):
    car = Car.objects.get(id=id)
    if request.user == car.owner:
        car.delete()
        messages.success(request,"Car is successfully removed")
        return redirect("/user/")
    else:
        messages.error(request,"This Car is not yours")
        return redirect("/user/")


def edit_car(request,id):
    car = Car.objects.get(id=id)
    user = request.user
    add = user.tennantaddress_set.all().get()
    numberofphotos = car.images.all().count()
    if request.method=="POST":
        usergroup = user.groups.all()
        group=usergroup.get()
        if group.name == 'owner':
            car.car_number = request.POST["car_number"]
            car.company = request.POST["company"]
            car.model = request.POST["model"]
            car.rent_price = request.POST["rent_price"]
            car.noofimage=request.POST["noofimage"]
            car.noofimage = int(car.noofimage)
            car.save()
            return render(request,"addcarimages.html",{"no_of_image":range(int(car.noofimage)),"carid":car.id,"noofimage":str(car.noofimage)})
        else:
            messages.error(request,"You are not authorised")
            return redirect("/")
    else:
        return render(request,"editcar.html",{"car":car,"add":add,"numberofphotos":numberofphotos})


@receiver(post_delete, sender=Car_Images)
def delete_product_image(sender, instance, **kwargs):
    instance.images.delete(False)