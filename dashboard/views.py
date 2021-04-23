from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from dashboard.models import Company,Update
from django.contrib.auth.models import User
# Create your views here.

path="http://127.0.0.1:8000/"

def adminlogin(request):
    if request.method=="GET":
        return render(request,'adminlogin.html')
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('companylist')
            else:
                return render(request,'adminlogin.html',{"error":"User is not a superuser"})
        else:
            return render(request,'adminlogin.html',{"error":"User does not exist"})

def clientlogin(request):
    if request.method=="GET":
        return render(request,'clientlogin.html')
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                return render(request,'clientlogin.html',{"error":"User is not a client"})
            else:
                login(request,user)
                return redirect('clientupdatelist')
        else:
            return render(request,'clientlogin.html',{"error":"User does not exist"})

def companylist(request):
    if request.user.is_authenticated and request.user.is_superuser:
        companies = Company.objects.all().order_by("-user__date_joined")
        if request.method=="POST":
            client_name=request.POST["clientname"]
            username=request.POST["username"]
            password=request.POST["password"]
            password2=request.POST["password2"]
            error=""
            if client_name=="":
                error="Client Name cannot be blank"
            elif username=="":
                error="Client ID cannot be blank"
            elif password=="":
                error="Set Password is blank, Please fill the form again"
            elif password2=="":
                error="Confirm Password is blank, Please fill the form again"
            if error!="":
                return render(request,'companylist.html',{"companies":companies,"error":error})
            if password!=password2:
                return render(request,'companylist.html',{"companies":companies,"error":"Password entered while confirming is different"})
            try:
                user = User.objects.create_user(username=username,password=password)
                Company.objects.create(user=user,name=client_name)
            except:
                return render(request,'companylist.html',{"companies":companies,"error":"Error while adding company, please try again"})
        return render(request,'companylist.html',{"companies":companies})

    else:
        return redirect('adminlogin')

def updatelist(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        company = Company.objects.get(id=id)
        updates = Update.objects.filter(company__id=id).order_by("id")
        if request.method=="POST":
            waste_category = request.POST["wastecategory"]
            waste_quantity = request.POST["wastequantity"]
            if waste_quantity=="":
                waste_quantity=0
            else:
                waste_quantity=int(waste_quantity)
            location = request.POST["location"]
            status = request.POST["status"]
            carbon_emission_saved = request.POST["ces"]
            certificate = request.FILES.get("certificate")
            error=""
            if waste_category=="":
                error="Waste Category can't be blank"
            elif waste_quantity<1:
                error="Waste Quantity should be greater than 0"
            elif location=="":
                error="Location can't be blank"
            elif status=="":
                error="Status can't be blank"
            elif carbon_emission_saved=="":
                error="Carbon Emission Saved can't be blank"
            elif status=="Completed" and certificate is None:
                error="Enter a certificate"
            
            if error!="":
                return render(request,'updatelist.html',{"updates":updates,"company":company,"error":error})
            u=Update.objects.create(
                company=company,
                waste_category=waste_category,
                waste_quantity=waste_quantity,
                location=location,
                status=status,
                carbon_emission_saved=carbon_emission_saved,
                certificate=certificate,
            )
            u.transaction_id="trc"+str(u.id)
            u.save()
        return render(request,'updatelist.html',{"updates":updates,"company":company})
    else:
        return redirect('adminlogin')

def update_detail(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        update = Update.objects.get(id=id)
        if request.method=="POST":
            waste_category = request.POST["wastecategory"]
            waste_quantity = int(request.POST["wastequantity"])
            location = request.POST["location"]
            status = request.POST["status"]
            carbon_emission_saved = request.POST["ces"]
            certificate = request.FILES.get("certificate")
            error=""
            if location=="":
                error="Location can't be blank"
            if carbon_emission_saved=="":
                error="Emission Saved can't be blank"
            
            if error!="":
                return render(request,'update_detail.html',{"update":update,"error":error})

            if waste_category is not None or waste_category!="":
                update.waste_category=waste_category
            if waste_quantity is not None and waste_quantity>1:
                update.waste_quantity=waste_quantity
            if location is not None and location!="":
                update.location=location
            if status is not None and status!="":
                update.status=status
            if carbon_emission_saved is not None and carbon_emission_saved!="":
                update.carbon_emission_saved=carbon_emission_saved
            if certificate is not None:
                update.certificate=certificate
            update.save()
            return render(request,'update_detail.html',{"update":update,"changes":"Changes Saved Successfully"})
        return render(request,'update_detail.html',{"update":update})
    else:
        return redirect('adminlogin')

def clientupdatelist(request):
    if request.user.is_authenticated and request.user.is_superuser is not True:
        company = Company.objects.get(user=request.user)
        updates = Update.objects.filter(company=company)
        return render(request,'clientupdatelist.html',{"updates":updates,"company":company})
    else:
        return redirect('clientlogin')

def clientupdatedetail(request,id):
    if request.user.is_authenticated and request.user.is_superuser is not True:
        update = Update.objects.get(id=id)
        return render(request,'clientupdatedetail.html',{"update":update})
    else:
        return redirect('clientlogin')

