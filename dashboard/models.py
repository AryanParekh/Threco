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
    filename='{}.{}'.format(instance.transaction_id,ext)
    return os.path.join("client_%s" % instance.company, filename)

class Company(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Update(models.Model):
    transaction_id = models.CharField(max_length=20)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    waste_category = models.CharField(max_length=12,choices=WASTE_CATEGORY_CHOICES)
    waste_quantity = models.IntegerField()
    state = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    status = models.CharField(max_length=12,choices=STATUS_CHOICES)
    certificate = models.ImageField(upload_to=get_upload_path,null=True,blank=True)
    carbon_emission_saved = models.CharField(max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.company)+" - "+str(self.transaction_id)




