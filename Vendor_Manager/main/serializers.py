from rest_framework import serializers
from .models import Vendor, PurchaseOrder, Performance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        # fields = 'id', 'name', 'contact_details' ,'address'
        fields = '__all__'


class POSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'

