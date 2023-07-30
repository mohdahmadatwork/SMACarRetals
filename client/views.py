from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth.models import Group
from orders.models import Order
from client.models import tennantaddress,Client_images
import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def dashboard(request):
    if(request.user.is_authenticated):
        if(request.method == 'POST'):
            client_id = request.POST["client_id"]
            email = request.POST["email"]
            if User.objects.filter(username__exact=email).exclude(id=client_id).exists():
                messages(request,"Choose different username!")
                return redirect('/user/')
            password = request.POST["password"]
            name = request.POST["name"]
            address = request.POST["address"]
            city = request.POST["city"]
            state = request.POST["state"]
            zip = request.POST["zip"]
            usertype = request.POST["usertype"]
            tenAdd = tennantaddress.objects.get(tennant=request.user)
            tenAdd.tennant_address = address
            tenAdd.city = city
            tenAdd.state = state
            tenAdd.zip = zip
            tenAdd.save()
            client = request.user
            client.username = email
            client.first_name = name
            client.password = password
            client.save()
            messages.success(request,"Profile successfully updated")
            return redirect('/user/')
        else:    
            user = request.user
            image = Client_images.objects.filter(user=user).get()
            add = user.tennantaddress_set.all().get()
            usertype = user.groups.all().get()
            cars = user.car_set.all()
            return render(request,"clientdashboard.html",{"user":user,"add":add,"usertype":usertype,"profile":image,"cars":cars})
    else:
        return redirect("/user/login/")
def handlelogin(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request , user)
            messages.success(request,"You are loged in as "+username)
            return redirect('/user/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/')
    else:
        return render(request,'login.html')
    
def handlesignup(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        password=request.POST["password"]
        type = request.POST["usertype"]
        address = request.POST["address"]
        state = request.POST["state"]
        city = request.POST["city"]
        zip = request.POST["zip"]
        user = User(first_name=name,username=email,password=password,email=email)
        user.save()
        useradd = tennantaddress(tennant=user,tennant_address = address ,state = state ,city = city ,zip = zip)
        if "dlimage" in request.FILES:
            if(len(request.FILES['dlimage'])!=0):
                useradd.dl = request.FILES['dlimage']
        else:
            useradd.delete()
            messages.warning(request,"You have to choose DL image")
            return redirect("/user/signup/")
        useradd.save()
        userprofileimg = Client_images()
        userprofileimg.user= user

        if(len(request.FILES["profileimage"])!=0):
                userprofileimg.images=request.FILES["profileimage"]
                userprofileimg.save()
        else:
            user.delete()
            useradd.delete()
            messages.error(request,"Some Error Occured")
            return redirect("/user/signup/")
        if type == "tenant":
            my_group = Group.objects.get(name='client') 
            my_group.user_set.add(user)
        else:
            my_group = Group.objects.get(name='owner') 
            my_group.user_set.add(user)
        messages.success(request,"Registered as "+name)
        login(request,user)
        return redirect("/")

    return render(request,"signup.html")  

def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('/')

@csrf_exempt
def editDlProfile(request):
    if(request.user.is_authenticated):
        if request.method=='POST' and request.FILES.get('image'):
            print("107 ")
            print(request.POST["title"])
            image_file = request.FILES.get('image')
            client_id = request.POST["client_id"]
            client = User.objects.get(id=client_id)
            if(request.user!=client):
                handlelogout()
                messages.error(request,"Something went wrong")
                return redirect('/')
            if(request.POST["title"]=="Driving License"):
                tenAdd = tennantaddress.objects.get(tennant = client)
                tenAdd.dl = image_file
                tenAdd.save()
                messages.success(request,"DL image successfully updated")
                return redirect('/user/')
            client_image_obj = Client_images.objects.get(user=client)
            client_image_obj.delete()
            client_image_obj = Client_images.objects.create(images=image_file,user=client)
            messages.success(request,"profile image successfully updated")
            return redirect('/user/')
        else:
            messages.error(request,"Something went wrong!")
            return redirect('/user/')
    else:
        messages.error(request,"Please Login!")
        return redirect('/login/')


def previousorderuserside(request):
    if request.user.is_authenticated:
        user = request.user
        groupname = user.groups.all().get().name
        if groupname == "client":
            orders = Order.objects.filter(tennant=user)
        else:
            orders=Order.objects.filter(Q(car__owner=user))
        orders = orders.order_by("-book_date")
        return render(request,"orders.html",{"orders":orders,"groupname":groupname,'date_now':datetime.datetime.now()})
    else:
        return redirect("/user/login/")