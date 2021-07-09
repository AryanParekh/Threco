from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("adminlogin/",views.adminlogin,name='adminlogin'),
    path("clientlogin/",views.clientlogin,name='clientlogin'),
    path("companylist/",views.companylist,name='companylist'),
    path("updatelist/<int:id>/",views.updatelist,name='updatelist'),
    path("update_detail/<int:id>/",views.update_detail,name='update_detail'),
    path("clientupdatelist/",views.clientupdatelist,name='clientupdatelist'),
    path("clientupdatedetail/<int:id>/",views.clientupdatedetail,name='clientupdatedetail'),
    path("downloadexcel/<int:id>/",views.downloadexcel,name='downloadexcel'),
    # SOCIETY COLLECTION
    path("api/collection_create/",views.SocietyCollectionCreate.as_view(),name="collection_create"),
    path("api/collection_edit/<int:pk>",views.SocietyCollectionCrud.as_view(),name="collection_edit"),
    path("api/collection_list/<str:username>",views.SocietyCollectionList,name="collection_list"),
    path("adminlogin2/",views.adminlogin2,name='adminlogin2'),
    path("societycollection/",views.societycollection,name='societycollection'),
    path("societycollectiondetail/<int:id>",views.societycollectiondetail,name='societycollectiondetail'),
    path("downloadexcel2/",views.downloadexcel2,name='downloadexcel2')
]