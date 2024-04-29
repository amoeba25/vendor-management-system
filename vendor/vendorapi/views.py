from django.shortcuts import render
from django.http import HttpResponse
from vendorapi.models import Vendor, PurchaseOrder
from vendorapi.serializers import VendorSerializer, PurchaseOrderSerializer, AcknowledgeSerializer, PerformanceSerializer
from rest_framework import generics
import random
from django.utils import timezone
from rest_framework.response import Response


# Create your views here.
def homepage(request):
    return HttpResponse("<h1> A Vendor Management System </h1>")

class VendorList(generics.ListCreateAPIView):
    """
    GET : List all the vendors
    POST : Create a new vendor
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET : Retrive a specific vendor details
    PUT : Update a specific vendor detail
    DELETE : Delete a specific vendor
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    

class PurchaseOrderList(generics.ListCreateAPIView):
    """
    GET : Get all the purchase order
    POST: Add a new purchase order
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET : Retrive a specific purchase order 
    PUT : Update a specific purchase order
    DELETE : Delete a purchase order
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    

class PurchaseOrderAcknowledge(generics.UpdateAPIView):
    """
    vendor can acknowledge the purchase order through 
    this endpoint
    POST : change acknowledgement date
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = AcknowledgeSerializer
    
    def perform_update(self, serializer):
        serializer.validated_data['acknowledgment_date'] = timezone.now()
        super().perform_update(serializer)
        return Response(serializer.data)
    

class VendorPerformance(generics.RetrieveAPIView):
    """
    fetches vendor performance metrics
    GET : fetch all performance metric for a specific vendor
    """
    queryset = Vendor.objects.all()
    serializer_class = PerformanceSerializer
    