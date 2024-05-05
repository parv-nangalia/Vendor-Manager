from django import dispatch
from django.dispatch import receiver
from .models import PurchaseOrder, Performance, Vendor
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Avg
from django.utils import timezone


#create_performance_model = dispatch.Signal()

# @receiver(create_performance_model)
# def performance_model(sender,request,**kwargs):
#     vendor_obj = Vendor.objects.get(pk=sender) 
#     obj = Performance.objects.create(vendor=vendor_obj,date=timezone.now(),on_time_delivery=0.0, quality_rating_avg=0.0, average_response_time=0.0,fulfillment_rate=0.0)
#     obj.save()

def update_vendor_details(obj):
    vendor_obj = Vendor.objects.get(pk=obj.vendor.id)    
    vendor_obj.on_time_delivery_rate = obj.on_time_delivery 
    vendor_obj.quality_rating_avg = obj.quality_rating_avg
    vendor_obj.average_response_time = obj.average_response_time
    vendor_obj.fullfillment_rate = obj.fulfillment_rate
    vendor_obj.save()
    return

po_status_changed = dispatch.Signal()

@receiver(po_status_changed)
def performance_metrics(sender,request,**kwargs):
    val = kwargs.get('arg')
    try:
        curr_obj = PurchaseOrder.objects.get(id=val)
    except ObjectDoesNotExist:
        print("no po found")
    try:
        obj = Performance.objects.filter(vendor=sender).latest('date')
    except ObjectDoesNotExist:
        obj = None
    
    vendor_pos = PurchaseOrder.objects.filter(vendor=sender)
    vendor_obj = Vendor.objects.get(pk=sender.id)

    new_obj = Performance.objects.create(
        vendor=vendor_obj,
        date=timezone.now(),
        on_time_delivery=obj.on_time_delivery if obj else 0.0,
        quality_rating_avg=obj.quality_rating_avg if obj else 0.0,
        average_response_time=obj.average_response_time if obj else 0.0,
        fulfillment_rate=obj.fulfillment_rate if obj else 0.0
    )
    
    if request.data['status'] == "Completed":
        otr = calculate_on_time_delivery_rate(vendor_pos)
        print("called_otr")
        new_obj.on_time_delivery = otr
    else:
        avr = calculate_fulfillment_rate(vendor_pos)
        new_obj.fulfillment_rate = avr
        print("called_fr")

    if(curr_obj.quality_rating is not None):
        qra = calculate_quality_rating_average(vendor_pos)
        new_obj.quality_rating_avg = qra
        print("called_qr")
    new_obj.save()
    update_vendor_details(new_obj)
    return



acknowledged = dispatch.Signal()

@receiver(acknowledged)
def Acknowledged_po(sender, request, **kwargs):
    print("acknowledge")

    try:
        obj = Performance.objects.filter(vendor=sender).latest('date')
    except ObjectDoesNotExist:
        obj = None

    vendor_obj = Vendor.objects.get(pk=sender) 
    new_obj = Performance.objects.create(
        vendor=vendor_obj,
        date=timezone.now(),
        on_time_delivery=obj.on_time_delivery if obj else 0.0,
        quality_rating_avg=obj.quality_rating_avg if obj else 0.0,
        average_response_time=obj.average_response_time if obj else 0.0,
        fulfillment_rate=obj.fulfillment_rate if obj else 0.0
    )

    vendor_pos = PurchaseOrder.objects.filter(vendor=sender)
    art = calculate_average_response_time(vendor_pos)
    new_obj.average_response_time = art
    new_obj.save()
    update_vendor_details(new_obj)
    return



##########################################################################################
##########################################################################################
########################################################################################


def calculate_on_time_delivery_rate(vendor_pos):
    total_completed_po = vendor_pos.filter(status='completed').count()
    quick_delivery = vendor_pos.filter(delivery_date__lte=timezone.now()).count()
    otr =  total_completed_po/quick_delivery
    return otr

def calculate_quality_rating_average(vendor_pos):
    avg_value = vendor_pos.filter(quality_rating__isnull=False).aggregate(avg_value=Avg('quality_rating'))['avg_value']
    return avg_value

def calculate_average_response_time(vendor_pos):
    avg_response = vendor_pos.aggregate(avg_time_diff=Avg(F('acknowledgment_date') - F('issue_date')))['avg_time_diff']
    print(avg_response)
    return avg_response

def calculate_fulfillment_rate(vendor_pos):
    total_completed_po = vendor_pos.filter(status='completed').count()
    total_po = vendor_pos.count()
    rate = total_completed_po/total_po
    return rate