from http.client import HTTPResponse
from inspect import trace
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from dashboard.models import Company,Update,UpdateWaste,SocietyCollection,Employee
from dashboard.serializers import SocietyCollectionSerializer
from django.contrib.auth.models import User
from rest_framework import generics,mixins,status
from django.http import JsonResponse
from io import BytesIO
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
import pandas as pd
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

def clientlogout(request):
    logout(request)
    return redirect('clientlogin')


def companylist(request):
    if request.user.is_authenticated and request.user.is_superuser:
        total=0
        etotal=0
        companies = Company.objects.all().order_by("-user__date_joined")
        employees = Employee.objects.all()
        for company in companies:
            all_update_waste=UpdateWaste.objects.filter(update__company=company)
            for each_update_waste in all_update_waste:
                total=total+each_update_waste.waste_quantity
                if each_update_waste.waste_category=="E Waste":
                    etotal=etotal+each_update_waste.waste_quantity
            company.total_waste=total
            company.e_waste=etotal
            company.save()
            #print(total)
            total=0
            etotal=0
        if request.method=="POST":
            print(request.POST)
            employeename=request.POST.get("employeename")
            print(employeename)
            if employeename==None:
                client_name=request.POST["clientname"]
                username=request.POST["username"]
                password=request.POST["password"]
                password2=request.POST["password2"]
                employee_name=request.POST.get("employee_name")
                print(employee_name)
                error=""
                if client_name=="":
                    error="Client Name cannot be blank"
                elif username=="":
                    error="Client ID cannot be blank"
                elif password=="":
                    error="Set Password is blank, Please fill the form again"
                elif password2=="":
                    error="Confirm Password is blank, Please fill the form again"
                elif employee_name=="":
                    error="Employee Name cannot be blank."
                if error!="":
                    return render(request,'companylist.html',{"companies":companies,"employees":employees,"error":error})
                if password!=password2:
                    return render(request,'companylist.html',{"companies":companies,"employees":employees,"error":"Password entered while confirming is different"})
                try:
                    user = User.objects.create_user(username=username,password=password)
                    Company.objects.create(user=user,name=client_name,point_of_contact=employee_name)
                except:
                    return render(request,'companylist.html',{"companies":companies,"employees":employees,"error":"Error while adding company, please try again"})
            else:
                try:
                    Employee.objects.create(name=employeename)
                except:
                    return render(request,'companylist.html',{"companies":companies,"employees":employees,"error":"Error while adding employee, please try again"})
        return render(request,'companylist.html',{"companies":companies,"employees":employees})

    else:
        return redirect('adminlogin')



def updatelist(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        company = Company.objects.get(id=id)
        employees=Employee.objects.all()
        #print(company)
        updates = Update.objects.filter(company__id=id).order_by("-id")
        for update in updates:
            if update.date_of_activity=="" or update.date_of_activity==None:
                update.date_of_activity=update.created_at
                update.save()
        sub_updates = UpdateWaste.objects.filter(update__company__id=id).order_by("-id")
        wastepie = [['Waste','Carbon Emission Saved']]
        statuspie = [["Status","No. of Updates"]]
        from django.db.models import Count
        result = UpdateWaste.objects.filter(update__company=company).values('status').annotate(dcount=Count('status')).order_by()
        for i in result:
            statuspie.append([i['status'],i['dcount']])
        wasteset = dict()
        for i in sub_updates:
            if i.waste_category in wasteset.keys():
                wasteset[i.waste_category]+=int(i.waste_quantity)
            else:
                wasteset[i.waste_category]=int(i.waste_quantity)
        for key,value in wasteset.items():
            wastepie.append([key,value])
        if request.method=="POST":
            error=""
            selected_waste = []
            selected_ces = []
            recycling_percentage=100
            for waste in WASTES:
                w1 = request.POST.get(waste+"-quantity")
                if w1 is not None:
                    if w1!="":
                        selected_waste.append([waste,int(w1)])
                    else:
                        error="Enter the waste amount"
            #state = request.POST["state"]
            #district = request.POST.get("district")
            status = request.POST["status"]
            employee_name=request.POST.get("employee_name")
            city=request.POST.get("city")
            certificate = request.FILES.get("certificate")
            date_of_activity=request.POST.get("date_of_activity")

            print(request.POST.get("city"))
            print(request.POST.get("employee_name"))
            print(request.POST.get("date_of_activity"))
            print(request.POST.get("date_of_activity"))
 
            """
            if state=="SELECT":
                error="State can't be blank"
            elif district is None or district=="":
                error="District can't be blank"
                """
            if status=="":
                error="Status can't be blank"
            elif status=="Completed" and certificate is None:
                error="Enter a certificate"
            if city is None or city=="":
                error="City can't be blank"
            if employee_name is None or employee_name=="":
                error="Employee Name can't be blank"
            if date_of_activity is None or date_of_activity=="":
                error="Date of Activity can't be blank"
            if len(selected_waste)==0:
                error="Fill at least one waste category"
            if error!="":
                return render(request,'updatelist.html',{"sub_updates":sub_updates,"company":company,"employees":employees,"error":error,"wastepie":wastepie,"statuspie":statuspie})
            if status=="Completed":
                for w in selected_waste:
                    x= request.POST.get(w[0]+"-quantityCE")
                    if x=="":
                        return render(request,'updatelist.html',{"sub_updates":sub_updates,"company":company,"employees":employees,"error":"Enter the C.E.S. for "+w[0],"wastepie":wastepie,"statuspie":statuspie})
                    else:
                        x=int(x)
                        selected_ces.append([w[0],x])
            u=Update.objects.create(
                    company=company,
                    status=status,
                    city=city,
                    employee_name=employee_name,
                    date_of_activity=date_of_activity,
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
                    #uw.certificate=certificate
                    uw.status=status
                    uw.save()
            wastepie = [['Waste','Carbon Emission Saved']]
            statuspie = [["Status","No. of Updates"]]
            from django.db.models import Count
            # result = Update.objects.values('status').annotate(dcount=Count('status')).order_by()
            result = Update.objects.filter(company=company).values('status').annotate(dcount=Count('status')).order_by()
            sub_updates = UpdateWaste.objects.filter(update__company__id=id).order_by("-id")
            for i in result:
                statuspie.append([i['status'],i['dcount']])
            wasteset = dict()
            for i in sub_updates:
                if i.waste_category in wasteset.keys():
                    wasteset[i.waste_category]+=int(i.waste_quantity)
                else:
                    wasteset[i.waste_category]=int(i.waste_quantity)
            for key,value in wasteset.items():
                wastepie.append([key,value])
            sub_updates = UpdateWaste.objects.filter(update__company__id=id).order_by("-id") 
            return render(request,'updatelist.html',{"sub_updates":sub_updates,"company":company,"employees":employees,"success":u.transaction_id+" added successfully","wastepie":wastepie,"statuspie":statuspie})
        return render(request,'updatelist.html',{"sub_updates":sub_updates,"company":company,"employees":employees,"wastepie":wastepie,"statuspie":statuspie})
    else:
        return redirect('adminlogin')

def delete_detail(request,id):
    waste=UpdateWaste.objects.get(id=id)
    error=""
    if request.method=="POST":
        waste.delete()
        error=waste.waste_category+ " "+"was deleted"
        trc=UpdateWaste.objects.filter(update__company=waste.update.company)
        print(trc)
        if not trc:
            particular_trc=waste.update
            particular_trc.delete()
        else:
            pass
        return render(request,'delete.html',{"waste":waste,"error":error})
    return render(request,'delete.html',{"waste":waste,"error":error})

def update_detail(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        true_sub_update=UpdateWaste.objects.get(id=id)
        print(true_sub_update.waste_category)
        update = Update.objects.get(id=true_sub_update.update.id)
        sub_updates = UpdateWaste.objects.filter(update=update)
        employees=Employee.objects.all()
        if request.method=="POST":
            error=""
            selected_waste = []
            selected_ces = []
            for waste in WASTES:
                w = request.POST.get(waste+"-quantity")
                if w is not None:
                    if w!="":
                        print(w)
                        print(type(w))
                        x = w.split(".", 1)
                        print(int(x[0])+1)
                        selected_waste.append([waste,int(x[0])])
                    else:
                        error="Enter the waste amount of "+waste[0]            
            #state = request.POST["state"]
            #district = request.POST.get("district")
            status = request.POST["status"]
            certificate = request.FILES.get("certificate")
            employee_name=request.POST.get("employee_name")
            city=request.POST.get("city")
            certificate = request.FILES.get("certificate")
            date_of_activity=request.POST.get("date_of_activity")
            recycling_percentage=request.POST.get("recycling_percentage")
            print(request.POST.get("city"))
            print(request.POST.get("employee_name"))
            print(request.POST.get("date_of_activity"))
            print(request.POST.get("date_of_activity"))
            """
            if district=="":
                error="District can't be blank"
            if state=="SELECT":
                error="State can't be blank"
                """
            if status=="Completed":
                for waste in selected_waste:
                    w = request.POST.get(waste[0]+"-quantityCE")
                    x = w.split(".", 1)
                    if w!="":
                            selected_ces.append([waste[0],int(x[0])])
                    else:
                        error="Enter the C.E.S amount of "+waste[0]
            if error!="":
                return render(request,'update_detail.html',{"update":update,"sub_updates":sub_updates,"employees":employees,"error":error})
            """
            if state is not None and state!="":
                update.state=state
            if district is not None and district!="":
                update.district=district
            """
            if city is not None and city!="":
                update.city=city
            if employee_name is not None and employee_name!="":
                update.employee_name=employee_name
            if status is not None and status!="":
                true_sub_update.status=status
            if date_of_activity is not None and date_of_activity!="":
                update.date_of_activity=date_of_activity
            if recycling_percentage is not None and recycling_percentage!="":
                true_sub_update.recycling_percentage=recycling_percentage
            if certificate is not None:
                true_sub_update.certificate=certificate
            update.save()
            true_sub_update.save()
            for waste,quantity in selected_waste:
                w=UpdateWaste.objects.get(waste_category=waste,update=update)
                w.waste_quantity=quantity
                w.save()
            if status=="Completed":
                for waste,ces in selected_ces:
                    w=UpdateWaste.objects.get(waste_category=waste,update=update)
                    w.carbon_emission_saved=ces
                    w.save()
            return render(request,'update_detail.html',{"update":update,"sub_updates":sub_updates,"employees":employees,"true_sub_update":true_sub_update})
        return render(request,'update_detail.html',{"update":update,"sub_updates":sub_updates,"employees":employees,"true_sub_update":true_sub_update})
    else:
        return redirect('adminlogin')

def clientupdatelist(request):
    if request.user.is_authenticated and request.user.is_superuser is not True:
        company = Company.objects.get(user=request.user)
        updates = Update.objects.filter(company=company).order_by('-id')
        sub_updates = UpdateWaste.objects.filter(update__company__id=company.id).order_by('-id')
        wastepie = [['Waste','Carbon Emission Saved']]
        statuspie = [["Status","No. of Updates"]]
        #statuspie=[]
        #wastepie=[]
        data=[20,30]
        from django.db.models import Count
        result = UpdateWaste.objects.filter(update__company=company).values('status').annotate(dcount=Count('status')).order_by()
        for i in result:
            statuspie.append([i['status'],i['dcount']])
        wasteset = dict()
        for i in sub_updates:
            if i.waste_category in wasteset.keys():
                wasteset[i.waste_category]+=int(i.waste_quantity)
            else:
                wasteset[i.waste_category]=int(i.waste_quantity)
        for key,value in wasteset.items():
            wastepie.append([key,value])
        return render(request,'clientupdatelist.html',{"company":company,"sub_updates":sub_updates,"wastepie":wastepie,"statuspie":statuspie,"data":data})
    else:
        return redirect('clientlogin')

def clientupdatedetail(request,id):
    if request.user.is_authenticated and request.user.is_superuser is not True:
        true_sub_update=UpdateWaste.objects.get(id=id)
        update = Update.objects.get(id=true_sub_update.update.id)
        sub_updates = UpdateWaste.objects.filter(update__id=update.id)
        if update.certificate:
            for updates in sub_updates:
                updates.certificate=update.certificate
                updates.save()
        subwastepie = [["Category","Carbon Emission Saved"]]
        for i in sub_updates:
            if i.carbon_emission_saved is not None:
                subwastepie.append([i.waste_category,int(i.carbon_emission_saved)])
            else:
                subwastepie.append([i.waste_category,0])
        return render(request,'clientupdatedetail.html',{"update":update,"sub_updates":sub_updates,"true_sub_update":true_sub_update,"subwastepie":subwastepie})
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
        """
        ws=wb.add_sheet("Transaction List")
        row_num = 0
        font_style=xlwt.XFStyle()
        font_style.font.bold=True

        columns = ['Transaction ID','City','Status']
        for col_num in range(len(columns)):
            ws.write(row_num,col_num,columns[col_num],font_style)
        
        font_style=xlwt.XFStyle()
        rows=updates.values_list('transaction_id','city','status')
        for row in rows:
            row_num+=1
            for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)
        """


        ws=wb.add_sheet(company.name)
        row_num = 0
        font_style=xlwt.XFStyle()
        font_style.font.bold=True

        columns = ['Transaction ID','Waste Category','Waste Quantity','City','Status']
        for col_num in range(len(columns)):
            ws.write(row_num,col_num,columns[col_num],font_style)
            
        font_style=xlwt.XFStyle()
        for update in updates:
            rows=UpdateWaste.objects.filter(update__company__id=id,update__transaction_id=update.transaction_id).values_list('update__transaction_id','waste_category','waste_quantity','update__city','status')
            for row in rows:
                row_num+=1
                for col_num in range(len(row)):
                    ws.write(row_num,col_num,str(row[col_num]),font_style)
    
        wb.save(response)
        return response
    else:
        return redirect('clientlogin')

def downloadexcel3(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            print("hi"+request.POST.get("month"))
    #companies=Company.objects.all().values_list('name')
    """
        reqd_months_update_wastes=UpdateWaste.objects.filter(update__date_of_activity__month=8 , update__date_of_activity__year=2022)
        company_name=reqd_months_update_wastes.values_list('update__transaction_id',flat=True)
        transaction_ids=reqd_months_update_wastes.values_list('update__company__name',flat=True)
        date = reqd_months_update_wastes.values_list('update__date_of_activity',flat=True)
        waste_categories = reqd_months_update_wastes.values_list('waste_category',flat=True)
        waste_quantity  = reqd_months_update_wastes.values_list('waste_quantity',flat=True)
        total_waste=reqd_months_update_wastes.aggregate(Sum('waste_quantity'))['waste_quantity__sum']
        df=pd.DataFrame()
        df['TransactionID']=transaction_ids
        df['Company Name']=company_name
        df['Waste Category']=waste_categories
        df['Waste Quantity']=waste_quantity
        df['Date of Pickup']=date
        df.loc[len(df.index)] = ["", "","",total_waste,""]

        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            # Set up the Http response.
            filename = 'July.xlsx'
            response = HttpResponse(
                b.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
            """
    return HttpResponse("Hello")

def downloadpage(request):
    import pandas as pd
    context={}
    if request.method=="POST":
        print("Hello")
        month=request.POST.get("month")
        year=request.POST.get("year")
        error=""
        if month=="" or month==None:
            error="Please enter Month"
        if year==""or year==None:
            error="Please enter Year"
        context={"error":error}
        reqd_months_update_wastes=UpdateWaste.objects.filter(update__date_of_activity__month=int(month) , update__date_of_activity__year=int(year))
        company_name=reqd_months_update_wastes.values_list('update__transaction_id',flat=True)
        transaction_ids=reqd_months_update_wastes.values_list('update__company__name',flat=True)
        date = reqd_months_update_wastes.values_list('update__date_of_activity',flat=True)
        waste_categories = reqd_months_update_wastes.values_list('waste_category',flat=True)
        waste_quantity  = reqd_months_update_wastes.values_list('waste_quantity',flat=True)
        total_waste=reqd_months_update_wastes.aggregate(Sum('waste_quantity'))['waste_quantity__sum']
        df=pd.DataFrame()
        df['TransactionID']=transaction_ids
        df['Company Name']=company_name
        df['Waste Category']=waste_categories
        df['Waste Quantity']=waste_quantity
        df['Date of Pickup']=date
        df.loc[len(df.index)] = ["", "","",total_waste,""]

        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            # Set up the Http response.
            filename = str(year)+"-"+str(month)+'.xlsx'
            response = HttpResponse(
                b.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
        return HttpResponse('Hi')
        
    return render(request,"download.html",context)

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



# SOCIETY PART

class SocietyCollectionCreate(mixins.CreateModelMixin,mixins.ListModelMixin, generics.GenericAPIView):
    queryset = SocietyCollection.objects.all()
    serializer_class = SocietyCollectionSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SocietyCollectionCrud(mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = SocietyCollection.objects.all()
    serializer_class = SocietyCollectionSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
class SocietyNameList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = SocietyCollection.objects.all()
        all_names=SocietyCollection.objects.all().values_list('society_name',flat=True)
        print(set(all_names))
        serializer = SocietyCollectionSerializer(snippets, many=True)
        content = {
            'status': set(all_names)
        }
        return Response(content)
   

@api_view(["GET"])
def SocietyCollectionList(request,username):
    if request.method=="GET":
        return JsonResponse(
            SocietyCollectionSerializer(SocietyCollection.objects.filter(employee_username=username).order_by("-created_at")[:3],many=True).data,
            status=status.HTTP_200_OK,
            safe=False,
        )
    else:
        return JsonResponse(
            data={"Message": "Only GET request allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

def adminlogin2(request):
    if request.method=="GET":
        return render(request,'adminlogin.html')
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('societycollection')
            else:
                return render(request,'adminlogin.html',{"error":"User is not a superuser"})
        else:
            return render(request,'adminlogin.html',{"error":"User does not exist"})

def societycollection(request):
    if request.user.is_authenticated and request.user.is_superuser:
        collection = SocietyCollection.objects.all().order_by('-created_at')
        return render(request,'societycollection.html',{"collection":collection})
    else:
        return redirect('adminlogin2')

def societycollectiondetail(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        collection = SocietyCollection.objects.get(id=id)
        return render(request,'societycollectiondetail.html',{"collection":collection})
    else:
        return redirect('adminlogin2')

def downloadexcel2(request):
    if request.user.is_authenticated and request.user.is_superuser:
        from django.http import HttpResponse
        import xlwt
        records = SocietyCollection.objects.all()
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition']='attachment; filename= Society Collection List.xls'
        wb = xlwt.Workbook(encoding='utf-8')

        ws=wb.add_sheet("Transaction List")
        row_num = 0
        font_style=xlwt.XFStyle()
        font_style.font.bold=True

        columns = ['Collection ID','Society Name','Contact Person','Contact Number','Society Location','Glass','Paper','Metal','Mix Plastic','PET Bottles','MLP Packaging','Tetrapack','Cartons','E-Waste','Hazardous Waste','Other Waste','Collected By','Collected At','Last Updated At']
        for col_num in range(len(columns)):
            ws.write(row_num,col_num,columns[col_num],font_style)
        
        font_style=xlwt.XFStyle()
        rows=records.values_list(
            "id",
            "society_name",
            "contact_person_name",
            "contact_no",
            "society_location",
            "glass",
            "paper",
            "metal",
            "mix_plastic",
            "pet_bottles",
            "mlp_packaging",
            "tetrapack",
            "cartons",
            "e_waste",
            "hazardous_waste",
            "other_waste",
            "employee_username",
            )
        for row in rows:
            row = list(row)
            record_id = SocietyCollection.objects.get(id=row[0])
            row.append(record_id.created_at.strftime("%Y-%m-%d %I:%M %p"))
            row.append(record_id.updated_at.strftime("%Y-%m-%d %I:%M %p"))
            row = tuple(row)
            row_num+=1
            for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)

        wb.save(response)
        return response
    else:
        return redirect('adminlogin2')





# DELETE TRANSACTIONS 
class DeleteTransaction(APIView):
    
    def get_object(self, pk):
        try:
            return Update.objects.get(pk=pk)
        except Update.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return HttpResponse("Deleted")

