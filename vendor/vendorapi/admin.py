from django.contrib import admin
from vendorapi.models import Vendor, PurchaseOrder, HistoricalPerformance

# Register your models here.
admin.site.register(Vendor)
admin.site.register(PurchaseOrder)