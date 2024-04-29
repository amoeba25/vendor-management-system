from rest_framework import serializers
from vendorapi.models import Vendor, PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
    
    # Make certain fields read-only
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        read_only_fields = ['vendor_code','on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fullfillment_rate']  # Add the fields you want to be read-only
        for field_name in read_only_fields:
            self.fields[field_name].read_only = True
    
    # Exclude read-only fields from the update
    def update(self, instance, validated_data):
        for field in self.Meta.fields:
            if field in self.fields and self.fields[field].read_only:
                validated_data.pop(field, None)
        return super().update(instance, validated_data)

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        
    # Make certain fields read-only
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        read_only_fields = ['po_number']  # Add the fields you want to be read-only
        for field_name in read_only_fields:
            self.fields[field_name].read_only = True
    
    # Exclude read-only fields from the update
    def update(self, instance, validated_data):
        for field in self.Meta.fields:
            if field in self.fields and self.fields[field].read_only:
                validated_data.pop(field, None)
        return super().update(instance, validated_data)
    
class AcknowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['acknowledgment_date']


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg',
                  'average_response_time', 'fullfillment_rate']