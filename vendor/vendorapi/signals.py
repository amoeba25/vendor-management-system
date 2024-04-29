from django.db.models.signals import post_save
from django.dispatch import receiver

from vendorapi.models import PurchaseOrder, HistoricalPerformance
from django.utils import timezone
from django.db.models import Avg, ExpressionWrapper, fields, F
from django.db.models.functions import ExtractHour
import math
from django.db import transaction

# Whenever Purchase Order changes, the signal triggers, updating the 
# Performance calculation metrics and Historical performance model

@receiver(post_save, sender = PurchaseOrder)
def performance_update(sender, instance, **kwargs):
    
    vendor = instance.vendor
    
    vendor_completed_po = PurchaseOrder.objects.filter(vendor = vendor, status = "completed")
    
    total_completed_po_count = vendor_completed_po.count()

    # on-time delivery percentage rate
    on_time_delivery_rate = vendor_completed_po.filter(delivery_date__lte = timezone.now()).count() / total_completed_po_count * 100 if total_completed_po_count > 0.0 else 0.0
    
    # average quality rating, rounded
    quality_rating_avg = vendor_completed_po.filter(quality_rating__isnull = False).aggregate(quality_rating_avg = Avg("quality_rating"))['quality_rating_avg']
    quality_rating_avg_rounded = round(quality_rating_avg, 3)
    
    # average response time
    acknowledged_pos = vendor_completed_po.filter(acknowledgment_date__isnull = False)
    
    # Calculate the difference between acknowledgment_date and issue_date for each instance
    response_times = [(pos.acknowledgment_date - pos.issue_date).total_seconds() / 3600  # Convert seconds to hours
                  for pos in acknowledged_pos]

    # Calculate the average response time in hours
    average_response_time = sum(response_times) / len(response_times) if response_times else 0.0
    average_response_time_rounded = round(average_response_time, 3)
    
    # fullfillment rate
    issued_po_count = PurchaseOrder.objects.filter(vendor = vendor).count()
    fullfillment_rate = total_completed_po_count / issued_po_count * 100 if issued_po_count else 0.0  
    
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg_rounded
    vendor.average_response_time = average_response_time_rounded
    vendor.fullfillment_rate = fullfillment_rate
    vendor.save()

    # atomic transaction gurantee
    with transaction.atomic():
        update_historical_performance = HistoricalPerformance.objects.create(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=round(average_response_time.total_seconds() /
                                        60 if average_response_time else 0.0, 2),
            fulLfillment_rate=fullfillment_rate,

        )