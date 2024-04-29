from django.urls import path
from vendorapi import views

urlpatterns = [
    path('', views.homepage, name="api-homepage"),
    path('vendors/', views.VendorList.as_view(), name="GetOrPostVendor"), 
    path('vendors/<int:pk>/', views.VendorDetail.as_view(), name="RetriveUpdateOrDeleteVendor"), 
    path('purchase_orders/', views.PurchaseOrderList.as_view(), name="GetOrPostPurchaseOrder"), 
    path('purchase_orders/<str:pk>', views.PurchaseOrderDetail.as_view(), name="RetriveUpdateOrDeletePurchaseOrder"), 
    path("vendors/<int:pk>/performance/", views.VendorPerformance.as_view(), name="FetchVendorPerformance"),
    path("purchase_orders/<str:pk>/acknowledge", views.PurchaseOrderAcknowledge.as_view(), name="VendorAcknowledge")
]