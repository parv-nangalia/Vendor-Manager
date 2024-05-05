from django.db import models
import uuid
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField(max_length=200)
    address = models.TextField(max_length=200)
    vendor_code = models.UUIDField( unique=True,default=uuid.uuid4, editable=False)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fullfillment_rate = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            self.vendor_code = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    po_number = models.UUIDField(max_length=5,default=uuid.uuid4,unique=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=30)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.po_number:
            self.po_number = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.po_number


class Performance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


    def __str__(self):
        return self.vendor