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

import os
def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename='{}.{}'.format("trc"+str(instance.id),ext)
    return os.path.join("client_%s" % instance.company, filename)

class Company(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Update(models.Model):
    transaction_id = models.CharField(max_length=20)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    state = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    status = models.CharField(max_length=12,choices=STATUS_CHOICES)
    certificate = models.ImageField(upload_to=get_upload_path,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.company)+" - "+str(self.transaction_id)

class UpdateWaste(models.Model):
    update = models.ForeignKey(Update,on_delete=models.CASCADE)
    waste_category = models.CharField(max_length=12,choices=WASTE_CATEGORY_CHOICES)
    waste_quantity = models.IntegerField()
    carbon_emission_saved=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.update)+" - "+str(self.waste_category)


# SOCIETY PART

class SocietyCollection(models.Model):
    society_name = models.CharField(max_length=100)
    contact_person_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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










