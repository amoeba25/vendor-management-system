from django.db import models
import random
import string

class Vendor(models.Model):
    """
    stores the essential information avout
    each and every vendor and their performance
    metrics
    """

    name = models.CharField(max_length=250, help_text="Name of the vendor")
    contact_details = models.TextField(help_text="Contact details of the vendor")
    address = models.TextField(help_text="Address of the vendor")
    vendor_code = models.CharField(unique= True, max_length= 10, help_text="Unique vendor code", blank=True)
    on_time_delivery_rate = models.FloatField(help_text="Percentage of on-time deliveries",blank=True, null=True)
    quality_rating_avg = models.FloatField(help_text="Average rating of quality based on product purchase",blank=True, null=True)
    average_response_time = models.FloatField(help_text="Average time taken to acknowledge purchase orders",blank=True, null=True)
    fullfillment_rate = models.FloatField(help_text="Percentage of orders that are fullfilled succesfully",blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        if not self.vendor_code:
            
            # generate an unique 6 digit code
            vendor_id = self.generate_vendor_id()
            self.vendor_code = vendor_id
        
        super().save(*args, **kwargs)
    
    def generate_vendor_id(self):
    # Use the vendor name to generate a unique vendorID
        data_hash = hash(self.name)
        random.seed(data_hash)
        vendor_id = random.randint(100000, 999999)  # Generate a random 6-digit number
        return str(vendor_id)
    
    
class PurchaseOrder(models.Model):
    """
    Details of each purchase order and is used to calculate
    various performance metrics 
    """
    
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled")
    )
    
    po_number = models.CharField(primary_key=True, max_length=6, unique=True, blank=True, help_text="Unique number for each purchase order") # making this the primary key
    vendor = models.ForeignKey(Vendor, blank=False, on_delete=models.CASCADE, help_text="Vendor associated with each purchase order")
    order_date = models.DateTimeField(auto_now_add=True, help_text="Date when order was placed")
    delivery_date = models.DateTimeField(help_text="Expected or actual delivery date")
    items = models.JSONField(help_text="Detials of the order")
    quantity = models.IntegerField(help_text="Total quantity of items in the purchase order")
    status = models.CharField(choices=STATUS_CHOICES, default="pending", max_length=20, help_text="Current status of the PO")
    quality_rating = models.FloatField(null=True, help_text="Rating given to the vendor for this PO")
    issue_date = models.DateTimeField(null=True, help_text="Timestamp for when PO was issued to the vendor")
    acknowledgment_date  = models.DateTimeField(help_text="Timestamp when the vendor acknowledged the PO")
    
    def __str__(self):
        return f"PO_{self.po_number}_{self.vendor}"
    
    def save(self, *args, **kwargs):
        if not self.po_number:
            self.po_number = self.generate_po_number()
        
        super().save(*args, **kwargs)
    
    # generating a random PO number on savng the model
    def generate_po_number(self):
        characters = string.ascii_uppercase + string.digits
        po_number = ''.join(random.choice(characters) for _ in range(6))
        return po_number
class HistoricalPerformance(models.Model):
    """
    stores historical vendor performance that is 
    used for trend analysis
    """
    
    vendor = models.ForeignKey(Vendor, blank=False, on_delete=models.CASCADE, help_text="Vendor associated with each purchase order")
    date = models.DateTimeField( help_text="Date of the performance recorded")
    historical_on_time_delivery_rate = models.FloatField(help_text="Historical record of on-time delivery rate")
    historical_quality_rating_avg = models.FloatField(help_text="Historical record of quality rating average")
    historical_average_response_time = models.FloatField(help_text="Historical record of average response time")
    historical_fullfillment_rate = models.FloatField(help_text="Historical record of the fullfillment rate")
    
    
