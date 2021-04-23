from django.urls import path
from . import views

urlpatterns=[
    path("adminlogin/",views.adminlogin,name='adminlogin'),
    path("clientlogin/",views.clientlogin,name='clientlogin'),
    path("companylist/",views.companylist,name='companylist'),
    path("updatelist/<int:id>/",views.updatelist,name='updatelist'),
    path("update_detail/<int:id>/",views.update_detail,name='update_detail'),
    path("clientupdatelist/",views.clientupdatelist,name='clientupdatelist'),
    path("clientupdatedetail/<int:id>/",views.clientupdatedetail,name='clientupdatedetail'),
]