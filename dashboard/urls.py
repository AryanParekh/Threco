from django.urls import path
from . import views
import django

urlpatterns=[
    path("adminlogin/",views.adminlogin,name='adminlogin'),
    path("",views.clientlogin,name='clientlogin'),
    path("logout/",views.clientlogout,name="clientlogout"),
    path("companylist/",views.companylist,name='companylist'),
    path("updatelist/<int:id>/",views.updatelist,name='updatelist'),
    path("update_detail/<int:id>/",views.update_detail,name='update_detail'),
    path("delete_detail/<int:id>/",views.delete_detail,name='delete_detail'),
    path("clientupdatelist/",views.clientupdatelist,name='clientupdatelist'),
    path("clientupdatedetail/<int:id>/",views.clientupdatedetail,name='clientupdatedetail'),
    path("downloadexcel/<int:id>/",views.downloadexcel,name='downloadexcel'),
    path("downloadexcel3/",views.downloadexcel3,name='downloadexcel3'),
    path("downloadexcel4/",views.downloadpage,name='downloadpage'),
    path("deletetransaction/<int:pk>/",views.DeleteTransaction.as_view(),name="deletetransaction"),
    # SOCIETY COLLECTION
    path("api/collection_create/",views.SocietyCollectionCreate.as_view(),name="collection_create"),
    path("api/collection_edit/<int:pk>",views.SocietyCollectionCrud.as_view(),name="collection_edit"),
    path("api/collection_list/<str:username>",views.SocietyCollectionList,name="collection_list"),
    path("adminlogin2/",views.adminlogin2,name='adminlogin2'),
    path("societycollection/",views.societycollection,name='societycollection'),
    path("societycollectiondetail/<int:id>",views.societycollectiondetail,name='societycollectiondetail'),
    path("downloadexcel2/",views.downloadexcel2,name='downloadexcel2'),
    path("societynames/",views.SocietyNameList.as_view()),
]