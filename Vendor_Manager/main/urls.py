from django.db import models

# Create your models here.
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from main import views
from main import authenticate as auth


urlpatterns = [

    path('', auth.HomepageAPIView.as_view(), name='home'),

    path('signup/', auth.SignupAPIView.as_view(), name='signup'),

    path('login/', auth.LoginAPIView.as_view(), name='login'),

    path('logout/', auth.LogoutAPIView.as_view(), name='logout'),


    path('api/vendor/', views.VendorListCreateAPIView.as_view() ,name='api-vendor'),
    # Endpoint for GET, POST for vendors
    
    path('api/vendor/<slug:pk>/', views.VendorDetailAPIView.as_view(), name='api-vendor-id'),   
    # Endpoint for details(GET), update(PUT), remove(DELETE) on vendor. 
    
    path('api/vendor/<slug:pk>/performance/', views.VendorPerformanceAPIView.as_view(), name='api-vendor-id-performance'),   
    # to direct all the other url paths to the 'main' app
    
    path('api/purchase_orders/', views.PurchaseOrderCreateAPIView.as_view(), name='api-po'),
    # 
    
    path('api/purchase_orders/<slug:po>/', views.PurchaseOrderDetailAPIView.as_view(),name='api-po-details'),
    #

    path('api/purchase_orders/<slug:po>/acknowledge', views.VendorAcknowledgeAPIView.as_view() , name='api-vendor-acknowledge'),


]


