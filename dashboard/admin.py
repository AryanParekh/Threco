from django.contrib import admin
from dashboard.models import Company,Update,UpdateWaste,SocietyCollection
# Register your models here.
admin.site.register(Company)
admin.site.register(Update)
admin.site.register(UpdateWaste)
admin.site.register(SocietyCollection)