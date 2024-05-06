from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder, Performance
from .serializers import VendorSerializer, POSerializer
from django.utils import timezone

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='9999999999')
        self.vendor2 = Vendor.objects.create(name='Vendor 2', contact_details='8888899999')

    def test_vendor_list_create_api(self):
        url = reverse('api-vendor')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        data = {'name': 'New Vendor', 'contact_details': '9999944774', 'address':'India'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 3)

    def test_vendor_detail_api(self):
        url = reverse('api-vendor-id', kwargs={'pk': self.vendor1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.vendor1.id)

    # Add more test methods for other vendor APIs...

class PurchaseOrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Vendor', contact_details='9999999999')
        self.po1 = PurchaseOrder.objects.create(vendor=self.vendor, order_date= '2024-05-05 15:30:00+05:30' , delivery_date= '2024-05-05 15:30:00+05:30', items= 'raw',quantity= 5,status='pending')
        self.po2 = PurchaseOrder.objects.create(vendor=self.vendor, order_date= '2024-05-05 15:30:00+05:30' , delivery_date= '2024-05-05 15:30:00+05:30', items= 'fresh',quantity= 8,status='pending')

    def test_purchase_order_create_api(self):
        url = reverse('api-po')
        print(self.po1.items, self.po2.items)
        data = {'vendor': self.vendor.id,'order_date': '2024-05-05 15:30:00+05:30', 'delivery_date': '2024-05-05 15:30:00+05:30', 'items': 'raw', 'quantity': '5', 'status': 'pending'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 3)

    def test_purchase_order_detail_api(self):
        url = reverse('api-po-details', kwargs={'po': self.po1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.po1.id)

    # Add more test methods for other purchase order APIs...

class VendorPerformanceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Vendor', contact_details='9999998888')
        self.performance1 = Performance.objects.create(vendor=self.vendor, on_time_delivery=0.8, date=timezone.now(), quality_rating_avg= 0.0, average_response_time= 0.0, fulfillment_rate = 0.0)
        self.performance2 = Performance.objects.create(vendor=self.vendor, on_time_delivery=0.9, date=timezone.now(), quality_rating_avg= 0.0, average_response_time= 0.0, fulfillment_rate = 0.0)


    def test_vendor_performance_api(self):
        url = reverse('api-vendor-id-performance', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)