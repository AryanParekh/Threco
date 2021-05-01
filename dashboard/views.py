from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from dashboard.models import Company,Update,UpdateWaste
from django.contrib.auth.models import User
# Create your views here.

WASTES = ["E Waste","Plastic","Paper","Metal","Others"]

def home(request):
    return render(request,'home.html')

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
        updates = Update.objects.filter(company__id=id).order_by("-id")
        sub_updates = UpdateWaste.objects.filter(update__company__id=id).order_by("-id") 
        wastepie = [['Waste','Carbon Emission Saved']]
        statuspie = [["Status","No. of Updates"]]
        from django.db.models import Count
        result = Update.objects.filter(company=company).values('status').annotate(dcount=Count('status')).order_by()
        for i in result:
            statuspie.append([i['status'],i['dcount']])
        wasteset = dict()
        for i in sub_updates:
            if i.waste_category in wasteset.keys():
                wasteset[i.waste_category]+=i.waste_quantity
            else:
                wasteset[i.waste_category]=i.waste_quantity
        for key,value in wasteset.items():
            wastepie.append([key,value])
        if request.method=="POST":
            error=""
            selected_waste = []
            selected_ces = []
            for waste in WASTES:
                w1 = request.POST.get(waste+"-quantity")
                if w1 is not None:
                    if w1!="":
                        selected_waste.append([waste,int(w1)])
                    else:
                        error="Enter the waste amount"
            state = request.POST["state"]
            district = request.POST.get("district")
            status = request.POST["status"]
            certificate = request.FILES.get("certificate")
            if state=="SELECT":
                error="State can't be blank"
            elif district is None or district=="":
                error="District can't be blank"
            elif status=="":
                error="Status can't be blank"
            elif status=="Completed" and certificate is None:
                error="Enter a certificate"
            if len(selected_waste)==0:
                error="Fill at least one waste category"
            if error!="":
                return render(request,'updatelist.html',{"sub_updates":sub_updates,"company":company,"error":error,"wastepie":wastepie,"statuspie":statuspie})
            if status=="Completed":
                for w in selected_waste:
                    x= request.POST.get(w[0]+"-quantityCE")
                    if x=="":
                        return render(request,'updatelist.html',{"sub_updates":sub_updates,"company":company,"error":"Enter the C.E.S. for "+w[0],"wastepie":wastepie,"statuspie":statuspie})
                    else:
                        x=int(x)
                        selected_ces.append([w[0],x])
            u=Update.objects.create(
                    company=company,
                    state=state,
                    district=district,
                    status=status,
                )
            u.transaction_id="trc"+str(u.id)
            if status=="Completed":
                u.certificate=certificate
            u.save()
            for category,quantity in selected_waste:
                UpdateWaste.objects.create(update=u,waste_category=category,waste_quantity=quantity)
            if status=="Completed":
                for category,ces in selected_ces:
                    uw = UpdateWaste.objects.get(update=u,waste_category=category)
                    uw.carbon_emission_saved=ces
                    uw.save()
            wastepie = [['Waste','Carbon Emission Saved']]
            statuspie = [["Status","No. of Updates"]]
            from django.db.models import Count
            result = Update.objects.values('status').annotate(dcount=Count('status')).order_by()
            for i in result:
                statuspie.append([i['status'],i['dcount']])
            wasteset = dict()
            for i in sub_updates:
                if i.waste_category in wasteset.keys():
                    wasteset[i.waste_category]+=i.waste_quantity
                else:
                    wasteset[i.waste_category]=i.waste_quantity
            for key,value in wasteset.items():
                wastepie.append([key,value])
            sub_updates = UpdateWaste.objects.filter(update__company__id=id).order_by("-id") 
            return render(request,'updatelist.html',{"sub_updates":sub_updates,"company":company,"success":u.transaction_id+" added successfully","wastepie":wastepie,"statuspie":statuspie})
        return render(request,'updatelist.html',{"sub_updates":sub_updates,"company":company,"wastepie":wastepie,"statuspie":statuspie})
    else:
        return redirect('adminlogin')

def update_detail(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        update = Update.objects.get(id=id)
        sub_updates = UpdateWaste.objects.filter(update=update)
        if request.method=="POST":
            error=""
            selected_waste = []
            selected_ces = []
            for waste in WASTES:
                w = request.POST.get(waste+"-quantity")
                if w is not None:
                    if w!="":
                        selected_waste.append([waste,int(w)])
                    else:
                        error="Enter the waste amount of "+waste[0]            
            state = request.POST["state"]
            district = request.POST.get("district")
            status = request.POST["status"]
            certificate = request.FILES.get("certificate")
            if district=="":
                error="District can't be blank"
            if state=="SELECT":
                error="State can't be blank"
            if status=="Completed":
                for waste in selected_waste:
                    w = request.POST.get(waste[0]+"-quantityCE")
                    if w!="":
                            selected_ces.append([waste[0],int(w)])
                    else:
                        error="Enter the C.E.S amount of "+waste[0]
            if error!="":
                return render(request,'update_detail.html',{"update":update,"sub_updates":sub_updates,"error":error})
            if state is not None and state!="":
                update.state=state
            if district is not None and district!="":
                update.district=district
            if status is not None and status!="":
                update.status=status
            if certificate is not None:
                update.certificate=certificate
            update.save()
            for waste,quantity in selected_waste:
                w=UpdateWaste.objects.get(waste_category=waste,update=update)
                w.waste_quantity=quantity
                w.save()
            if status=="Completed":
                for waste,ces in selected_ces:
                    w=UpdateWaste.objects.get(waste_category=waste,update=update)
                    w.carbon_emission_saved=ces
                    w.save()
            return render(request,'update_detail.html',{"update":update,"sub_updates":sub_updates})
        return render(request,'update_detail.html',{"update":update,"sub_updates":sub_updates})
    else:
        return redirect('adminlogin')

def clientupdatelist(request):
    if request.user.is_authenticated and request.user.is_superuser is not True:
        company = Company.objects.get(user=request.user)
        updates = Update.objects.filter(company=company).order_by('-id')
        sub_updates = UpdateWaste.objects.filter(update__company__id=company.id).order_by('-id')
        wastepie = [['Waste','Carbon Emission Saved']]
        statuspie = [["Status","No. of Updates"]]
        from django.db.models import Count
        result = Update.objects.filter(company=company).values('status').annotate(dcount=Count('status')).order_by()
        for i in result:
            statuspie.append([i['status'],i['dcount']])
        wasteset = dict()
        for i in sub_updates:
            if i.waste_category in wasteset.keys():
                wasteset[i.waste_category]+=i.waste_quantity
            else:
                wasteset[i.waste_category]=i.waste_quantity
        for key,value in wasteset.items():
            wastepie.append([key,value])
        return render(request,'clientupdatelist.html',{"company":company,"sub_updates":sub_updates,"wastepie":wastepie,"statuspie":statuspie})
    else:
        return redirect('clientlogin')

def clientupdatedetail(request,id):
    if request.user.is_authenticated and request.user.is_superuser is not True:
        update = Update.objects.get(id=id)
        sub_updates = UpdateWaste.objects.filter(update__id=id)
        subwastepie = [["Category","Carbon Emission Saved"]]
        for i in sub_updates:
            if i.carbon_emission_saved is not None:
                subwastepie.append([i.waste_category,i.carbon_emission_saved])
            else:
                subwastepie.append([i.waste_category,0])
        return render(request,'clientupdatedetail.html',{"update":update,"sub_updates":sub_updates,"subwastepie":subwastepie})
    else:
        return redirect('clientlogin')

def downloadexcel(request,id):
    if request.user.is_authenticated:
        from django.http import HttpResponse
        import xlwt
        company = Company.objects.get(id=id)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition']='attachment; filename= Transaction List of ' +company.name+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')

        updates = Update.objects.filter(company=company)
        ws=wb.add_sheet("Transaction List")
        row_num = 0
        font_style=xlwt.XFStyle()
        font_style.font.bold=True

        columns = ['Transaction ID','State','District','Status']
        for col_num in range(len(columns)):
            ws.write(row_num,col_num,columns[col_num],font_style)
        
        font_style=xlwt.XFStyle()
        rows=updates.values_list('transaction_id','state','district','status')
        for row in rows:
            row_num+=1
            for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)



        for update in updates:
            ws=wb.add_sheet(update.transaction_id)
            row_num = 0
            font_style=xlwt.XFStyle()
            font_style.font.bold=True

            columns = ['Transaction ID','Waste Category','Waste Quantity','State','District','Status']
            for col_num in range(len(columns)):
                ws.write(row_num,col_num,columns[col_num],font_style)
            
            font_style=xlwt.XFStyle()
            rows=UpdateWaste.objects.filter(update__company__id=id,update__transaction_id=update.transaction_id).values_list('update__transaction_id','waste_category','waste_quantity','update__state','update__district','update__status')
            for row in rows:
                row_num+=1
                for col_num in range(len(row)):
                    ws.write(row_num,col_num,str(row[col_num]),font_style)
    
        wb.save(response)
        return response
    else:
        return redirect('clientlogin')




# Random Update Generator Code :
    # import random
    # for i in range(25):
    #     cat = ["E Waste","Paper","Plastic","Metal","Others"]
    #     loc = ["Mumbai","Pune","Ahemdabad","Nashik","Sikkim"]
    #     company = Company.objects.get(id=id)
    #     u=Update.objects.create(
    #                 company=company,
    #                 waste_category=random.choice(cat),
    #                 waste_quantity=random.randint(1,1000),
    #                 location=random.choice(loc),
    #                 status="In Process",
    #                 carbon_emission_saved="-",
    #             )
    #     u.transaction_id="trc"+str(u.id)
    #     u.save()