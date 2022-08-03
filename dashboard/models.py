from django.db import models
from django.contrib.auth.models import User
# Create your models here.

WASTE_CATEGORY_CHOICES=(
    ("E Waste","E Waste"),
    ("Paper","Paper"),
    ("Plastic","Plastic"),
    ("Metal","Metal"),
    ("Others","Others"),
)

STATUS_CHOICES=(
    ("In Process","In Process"),
    ("Completed","Completed"),
)

EMPLOYEE_CHOICES=(
    ("Sharika Dhar","Sharika Dhar"),
    ("Roocha", "Roocha" ),
)
import os
def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename='{}.{}'.format("trc"+str(instance.id),ext)
    return os.path.join("client_%s" % instance.update.company, filename)

def get_upload_path2(instance, filename):
    ext = filename.split('.')[-1]
    filename='{}.{}'.format("trc"+str(instance.id),ext)
    return os.path.join("client_%s" % instance.company, filename)

class Employee(models.Model):
    name=models.CharField(max_length=255,null=True)
    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return "hi"

class Company(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    point_of_contact=models.CharField(max_length=255, default="Sharika Dhar", choices=EMPLOYEE_CHOICES)
    #point_of_contact=models.ForeignKey(on_delete=models.CASCADE, default=Employee.objects.first())
    total_waste=models.IntegerField(null=True,default=0)
    e_waste=models.IntegerField(null=True,default=0)
    def __str__(self):
        return self.name

class Update(models.Model):
    transaction_id = models.CharField(max_length=20)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=200, default="Roocha")
    district = models.CharField(max_length=200, default="Maharashtra")
    city = models.CharField(max_length=200, default="Mumbai")
    status = models.CharField(max_length=12,choices=STATUS_CHOICES)
    certificate = models.ImageField(upload_to=get_upload_path2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=False,null=True)
    updated_at = models.DateTimeField(auto_now=True,  null=True)
    date_of_activity = models.DateField(auto_now_add=False, null=True)
    note = models.TextField(null=True,blank=True)
    recycling_percentage=models.IntegerField(null=True, default=100)
    def __str__(self):
        return str(self.company)+" - "+str(self.transaction_id)

class UpdateWaste(models.Model):
    update = models.ForeignKey(Update,on_delete=models.CASCADE)
    waste_category = models.CharField(max_length=12,choices=WASTE_CATEGORY_CHOICES)
    waste_quantity = models.DecimalField(decimal_places=2,max_digits=7)
    incineration_rate = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=7)
    landfill_rate = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=7)
    recycling_rate = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=7)
    carbon_emission_saved=models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=7)
    certificate = models.ImageField(upload_to=get_upload_path,null=True,blank=True)
    recycling_percentage=models.IntegerField(null=True, default=100)
    status = models.CharField(max_length=12,choices=STATUS_CHOICES,default="In Process")
    def __str__(self):
        return str(self.update)+" - "+str(self.waste_category)


# SOCIETY PART

class SocietyCollection(models.Model):
    society_name = models.CharField(max_length=100)
    contact_person_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_of_activity = models.DateField(auto_now_add=False, null=True)
    society_location = models.CharField(max_length=300)
    employee_username = models.CharField(max_length=100)
    glass = models.FloatField(default=0,null=True,blank=True)
    paper = models.FloatField(default=0,null=True,blank=True)
    metal = models.FloatField(default=0,null=True,blank=True)
    mix_plastic = models.FloatField(default=0,null=True,blank=True)
    pet_bottles = models.FloatField(default=0,null=True,blank=True)
    mlp_packaging = models.FloatField(default=0,null=True,blank=True)
    tetrapack = models.FloatField(default=0,null=True,blank=True)
    cartons = models.FloatField(default=0,null=True,blank=True)
    e_waste = models.FloatField(default=0,null=True,blank=True)
    hazardous_waste = models.FloatField(default=0,null=True,blank=True)
    other_waste = models.FloatField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.society_name)+" - "+str(self.created_at)











