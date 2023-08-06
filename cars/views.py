from django.shortcuts import render,redirect
from cars.models import Car,Car_Images,Caraddress
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib import messages
from cars.forms import CarImagesForm
from client.models import tennantaddress
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from datetime import datetime
# Create your views here.
def available_cars(request):
    current_date = datetime.now().date().strftime('%Y-%m-%d')
    if not request.user.is_authenticated:
        cars = Car.objects.all()
        if request.method == "POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            if(datetime.strptime(to_date,'%Y-%m-%d')<datetime.strptime(current_date ,'%Y-%m-%d') or datetime.strptime(from_date,'%Y-%m-%d')<datetime.strptime(current_date ,'%Y-%m-%d')):
                messages.error(request,"Kindly choose a valid date")
                user = request.user
                add = tennantaddress(tennant=user)
                return render(request,"order.html",{"id":id,"add":add,"cur_date":current_date})
            ordered_car_ids = Order.objects.filter(
                from_date__lte=to_date,
                to_date__gte=from_date
            ).values_list('car_id', flat=True)
            
            cars = cars.exclude(id__in=ordered_car_ids)
        return render(request,'availablecars.html',{"cars":cars})
    else:
        user = request.user
        group = user.groups.all().get()
        groupname = group.name
        if groupname == "client":
            cars = Car.objects.all()
            if request.method == "POST":
                from_date = request.POST["from_date"]
                to_date = request.POST["to_date"]
                if(datetime.strptime(to_date,'%Y-%m-%d')<datetime.strptime(current_date ,'%Y-%m-%d') or datetime.strptime(from_date,'%Y-%m-%d')<datetime.strptime(current_date ,'%Y-%m-%d')):
                    messages.error(request,"Kindly choose a valid date")
                    user = request.user
                    add = tennantaddress(tennant=user)
                    return render(request,"order.html",{"id":id,"add":add,"cur_date":current_date})
                ordered_car_ids = Order.objects.filter(
                    from_date__lte=to_date,
                    to_date__gte=from_date
                ).values_list('car_id', flat=True)
                
                cars = cars.exclude(id__in=ordered_car_ids)
                return render(request,'availablecars.html',{"cars":cars})
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
            
            car=Car ()
            car.car_number = request.POST["car_number"]
            car.company = request.POST["company"]
            car.model = request.POST["model"]
            car.rent_price = request.POST["rent_price"]
            noofimage=request.POST["noofimage"]
            car.noofimage = int(noofimage)
            car.fine = request.POST["fine"]
            car.cancel_charge = request.POST["cancel_charge"]
            car.owner = user
            car.availablity = True
            car.save()
            add = Caraddress()
            add.car = car
            add.tennant_address = request.POST["address"]
            add.city = request.POST["city"]
            add.state = request.POST["state"]
            add.zip = request.POST["zip"]
            add.save()
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

def delete_car_image(request,id):
    try:
        car_image = Car_Images.objects.get(id=id)
        print(car_image)
        car_image.delete()
        message = {"message":True}
        return JsonResponse(message)
    except Car_Images.DoesNotExist:
        message = {"message":False}
        return JsonResponse(message)
    except:
        message = {"message":False}
        return JsonResponse(message)
    
@csrf_exempt
def upload_image(request):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            car_id = request.POST.get('car_id')
            car = Car.objects.get(id=car_id)
            if(car.owner != request.user):
                messages.error(request,"Something went wrong!")
                return redirect('/cars/') 
            for i in range(len(request.FILES)):
                nameOfImage = 'image'+str(i)
                image_file = request.FILES[nameOfImage]
                uploaded_image = Car_Images.objects.create(images=image_file,car = car)
            return JsonResponse({'status': 'success', 'image_url': uploaded_image.images.url})
        else:
            return JsonResponse({'status': 'error', 'message': 'No image file received.','image_files':request.FILES})
    else:
        messages.error(request,"Something went wrong!")
        return redirect('/cars/') 
    
def edit_car(request,id):
    car = Car.objects.get(id=id)
    user = request.user
    add = car.caraddress_set.all().get()
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
            car.fine = request.POST["fine"]
            car.cancel_charge = request.POST["cancel_charge"]
            car.save()
            add.tennant_address = request.POST["address"]
            add.city = request.POST["city"]
            add.state = request.POST["state"]
            add.zip = request.POST["zip"]
            add.save()
            messages.success(request,"Car saved successfully.")
            return redirect("/")
        else:
            messages.error(request,"You are not authorised")
            return redirect("/")
    else:
        return render(request,"editcar.html",{"car":car,"add":add,"numberofphotos":numberofphotos})


@receiver(post_delete, sender=Car_Images)
def delete_product_image(sender, instance, **kwargs):
    instance.images.delete(False)