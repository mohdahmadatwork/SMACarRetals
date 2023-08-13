from django.shortcuts import render,redirect
from cars.models import Car
from client.models import tennantaddress
from orders.models import Order,CancelOrder
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate,logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.
def make_order(request,id):
    if request.user.is_authenticated:
        current_date = datetime.now().date().strftime('%Y-%m-%d')
        if request.method=="POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            if(datetime.strptime(to_date,'%Y-%m-%d')<datetime.strptime(current_date ,'%Y-%m-%d') or datetime.strptime(from_date,'%Y-%m-%d')<datetime.strptime(current_date ,'%Y-%m-%d')):
                messages.error(request,"Kindly choose a valid date")
                user = request.user
                add = tennantaddress(tennant=user)
                return render(request,"order.html",{"id":id,"add":add,"cur_date":current_date})
            car = Car.objects.get(id=id)
            orders_for_car = Order.objects.filter(car=car, from_date__lte=from_date, to_date__gte=from_date).exists()
            if(orders_for_car):
                messages.error(request,"This car is not available on your time!")
                return redirect("/orders/{id}")
            user = request.user
            groups = user.groups.all()
            group=groups.get()
            if group.name == "client": 
                order = Order()
                order.car = car
                order.tennant = request.user
                order.from_date = from_date
                order.to_date = to_date
                order.price_per_day = order.car.rent_price
                order.price =(datetime.strptime(to_date,'%Y-%m-%d')-datetime.strptime(from_date,'%Y-%m-%d')).days * order.price_per_day
                order.tennant_address = request.POST["tennant_address"]
                order.city = request.POST["city"]
                order.state = request.POST["state"]
                order.zip = request.POST["zip"]
                for key, value in request:
                    print(f"Key: {key}, Value: {value}")
                if(request.FILES.get('dl')):
                    order.dl = request.FILES["dl"]
                order.car.availablity=False
                order.car.save()
                order.save()
                messages.success(request,"Car is booked")
                return redirect("/")
            else:
                messages.warning(request,"Car is unable to book")
                return redirect("/")
        user = request.user
        add = tennantaddress(tennant=user)
        return render(request,"order.html",{"id":id,"add":add,"cur_date":current_date})
    else:
        messages.warning(request,"Please sign in to rent a car!")
        return redirect("/cars/")
@csrf_exempt
def checkAvailability(request):
    if request.user.is_authenticated and request.method=="POST":
        car_id = request.POST["car_id"]
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        if to_date is None:
            to_date = from_date
        if from_date:
            car = Car.objects.get(id=car_id)
            orders_for_car = Order.objects.filter(
                car=car, 
                from_date__lte=to_date,
                to_date__gte=from_date,
                cancel_b = False,
            ).filter(
                Q(return_b=True) | Q(return_b=False, return_date__isnull=True)
            ).exists()
            if(orders_for_car):
                response = {"message":"This car is not available on your time!","status":"455"}
                return JsonResponse(response)
            else:
                response = {"message":"This car is available on your time!","status":"200"}
                return JsonResponse(response)

        else:
            response = {"message":"From Date can not be empty!","status":"400"}
            return JsonResponse(response)
    else:
        response = {"message":"Not authorized!","status":"500"}
        return JsonResponse(response)



def return_car(request):
    if request.method == "POST":
        user = authenticate(username=request.user.username,password=request.POST["password"])
        print(user)
        print(request.user)
        if user is not None:
            car = Car.objects.get(car_number=request.POST["carnumber"])
            if car.owner == request.user:
                order = Order.objects.get(car=car,return_b=False)
                user = request.user
                groups = user.groups.all()
                group = groups.get()
                if group.name == "owner":
                    car.availablity = True
                    car.save()
                    order.return_b=True
                    order.return_date=datetime.now()
                    if(datetime.strftime(order.to_date,'%Y-%m-%d') < datetime.now().date().strftime('%Y-%m-%d')):
                        order.late_charge = (datetime.strptime(order.return_date,'%Y-%m-%d')-datetime.strptime(order.to_date,'%Y-%m-%d')).days * order.price_per_day + (datetime.strptime(order.return_date,'%Y-%m-%d')-datetime.strptime(order.to_date,'%Y-%m-%d')).days * car.fine
                        order.price = order.price + order.late_charge
                        order.late_b = True
                    order.save()
                    messages.success(request,"Car return successfully")
                return redirect("/cars/")
            else:
                messages.error(request,"The Car don't belongs to you")
                return redirect("/")
        else:
            messages.error(request,"Wrong Password!")
            return redirect("/")
    else:
        logout(request)
        messages.error(request,"You are not Authorised")
        return redirect("/")

def order_detail(request,id):
    order=Order.objects.get(id=id)
    return render(request,"orderdetails.html",{"order":order})

def re_rent(request,id):
    current_date = datetime.now().date().strftime('%Y-%m-%d')
    if request.method=="POST":
        if(datetime.strptime(order.to_date,'%Y-%m-%d')<current_date or datetime.strptime(order.from_date,'%Y-%m-%d')<current_date):
           messages.error(request,"Kindly choose a valid date")
           user = request.user
           add = tennantaddress(tennant=user)
           return render(request,"order.html",{"id":id,"add":add,"cur_date":current_date})
        user = request.user
        groups = user.groups.all()
        group=groups.get()
        if group.name == "client": 
            order = Order()
            order.car = Car.objects.get(id=id)
            if order.car.availablity:
                order.tennant = request.user
                order.from_date = request.POST["from_date"]
                order.to_date = request.POST["to_date"]
                order.price_per_day = order.car.rent_price
                order.price =(datetime.strptime(order.to_date,'%Y-%m-%d')-datetime.strptime(order.from_date,'%Y-%m-%d')).days * order.price_per_day
                order.tennant_address = request.POST["tennant_address"]
                order.city = request.POST["city"]
                order.state = request.POST["state"]
                order.zip = request.POST["zip"]
                if "dl" in request.FILES:
                    if(len(request.FILES.get('dl'))!=0):
                        order.dl = request.FILES["dl"]
                else:
                    order.dl=user.tennantaddress_set.all().get().dl
                order.car.availablity=False
                order.car.save()
                order.save()
                messages.success(request,"Car is booked")
                return redirect("/")
            else:
                messages.warning(request,"Car is not available")
                return redirect("/cars/")
        else:
            messages.warning(request,"Car is unable to book")
            return redirect("/")
    else:
        user = request.user
        previous_order = Order.objects.get(id=id)
        return render(request,"re_order.html",{"previous_order":previous_order,"user":user,"cur_date":current_date})

def cancel_order(request,id):
    order = Order.objects.get(id=id)
    if order.from_date > timezone.now():
        if not(order.cancel_b==True or order.return_b==True):
            order.cancel_b = True
            order.cancel_charge = order.car.cancel_charge
            order.price = order.cancel_charge
            order.car.availablity=True
            order.car.save()
            order.save()
            cancelorder = CancelOrder(order=order)
            cancelorder.save()
            messages.success(request,"Order has been cancelled successfully ")
            return redirect("/")
        else:
            messages.error(request,"Car is already Returned Or cancelled")
            return redirect("/user/previousorder")
    else:
        messages.error(request ,"You can not cancel the order as order period started already")
        return redirect("/user/previousorder")