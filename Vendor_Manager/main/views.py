from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor, Performance, PurchaseOrder
from .serializers import VendorSerializer, POSerializer, PerformanceSerializer
from django.utils import timezone
from .signals import po_status_changed, acknowledged
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class VendorListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor = Vendor.objects.all()
        serializer = VendorSerializer(vendor, many=True)
        json_data = { "name": "JOe",
                        "contact_details": "8793223432",
                        "address": "hello world 2" }
        
        response_data = {
            "SAMPLE_FORM_DATA": json_data,
            "------------":"------------ ",
            "-----------":"------------",
            "vendor_data": serializer.data
           
        }
        return Response(response_data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # create_performance_model.send(sender=serializer.data['id'],request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VendorDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return None

    def get(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class PurchaseOrderCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        po = PurchaseOrder.objects.all()
        serializer = POSerializer(po, many=True)
        json_data = {
            "order_date": "2024-05-04T10:00:00Z",
            "delivery_date": "2024-05-10T10:00:00Z",
            "items": "milk",
            "quantity": 5,
            "status": "Pending",
            "quality_rating": 7.7,
            "vendor": 1 
        }
        
        response_data = {
            "SAMPLE_FORM_DATA": json_data,
            "------------":"------------ ",
            "-----------":"------------",
            "purchase_order": serializer.data
           
        }

        return Response(response_data)


    def post(self, request):
        serializer = POSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PurchaseOrderDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, po):
        try:
            return PurchaseOrder.objects.get(pk=po)
        except PurchaseOrder.DoesNotExist:
            return None

    def get(self, request, po):
        porder = self.get_object(po)
        if porder is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = POSerializer(porder)
        return Response(serializer.data)

    def put(self, request, po):
        porder = self.get_object(po)
        if porder is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        print(request.data)
        serializer = POSerializer(porder, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            if "status" in request.data:
                print("calling signal")
                po_status_changed.send(sender=porder.vendor,request=request,arg = porder.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po):
        porder = self.get_object(po)
        if porder is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        porder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorPerformanceAPIView(APIView):
    # def get_object(self, pk):
    #     try:
    #         return Performance.objects.get(vendor=pk)
    #     except Performance.DoesNotExist:
    #         return None
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        performance = Performance.objects.filter(vendor=pk)
        serializer = PerformanceSerializer(performance, many=True)
        return Response(serializer.data)

class VendorAcknowledgeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, po):
        try:
            return PurchaseOrder.objects.get(pk=po)
        except PurchaseOrder.DoesNotExist:
            return None
        
    def post(self,request,po):
        porder = self.get_object(po)
        if porder is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            porder.acknowledgment_date = timezone.now()
            vendor = porder.vendor
            serializer = POSerializer(porder, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                acknowledged.send(sender=vendor.id,request=request)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

