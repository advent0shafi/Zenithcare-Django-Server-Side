from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from authentification.models import User
from django.core import serializers
from authentification.serializers import UserSerializers
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from vendor.models import Therapist
from payment.models import Payment
from payment.serializers import PaymentStatisticsSerializer ,Payment_Booked_Serializer
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import Cast, Coalesce
from vendor_booking.models import Booking
from .serializers import AdminStatisticalDataSerializer,ReportTherapistList
from rest_framework import generics
from .models import TherapistReport
from .serializers import ReportSerializer
from vendor.models import Category,Language
from vendor.serializers import CategorySerializer,LanguageSerializer

# Create your views here.
class UserList(APIView):
    permission_classes  = [IsAdminUser]

    def get(self, request):

        userlist = User.objects.filter(is_superuser=False)
        data = {
                'userlist': userlist.values('id','password','username', 'email','profile_img','is_active','is_therapist','is_verified','phone_number','is_superuser')  
            
            }
        return Response(data)


class VendorList(APIView):
    permission_classes  = [IsAdminUser]

    def get(self, request):

        userlist = User.objects.filter(is_therapist=True)
        data = {
                'userlist': userlist.values('id','password','username', 'email','profile_img','is_active','is_therapist','is_verified','phone_number','is_superuser')  
            }
        return Response(data)
    
class PendingVerifyList(APIView):
    permission_classes  = [IsAdminUser]

    def get(self, request):
        # Filter users who have a corresponding Therapist model
        userlist = User.objects.filter(therapist__isnull=False)

        data = {
            'userlist': userlist.values('id', 'password', 'username', 'email', 'profile_img', 'is_active', 'is_therapist', 'is_verified', 'phone_number', 'is_superuser')  
        }

        return Response(data)


class UserBlock(APIView):
    # permission_classes  = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            user.is_active = not user.is_active  # Toggle the is_active status
            user.save()

            serializer = UserSerializers(user)  # Update with your serializer
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class VendorApprove(APIView):
    # permission_classes  = [IsAdminUser]

    def post(self,request,user_id):

        try:
            user = get_object_or_404(User, id=user_id)
            user.is_therapist= not user.is_therapist  
            user.save()

            serializer = UserSerializers(user)  # Update with your serializer
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        

class PaymentStatisticsAPI(APIView):
    permission_classes  = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        total_amount_received = Payment.objects.filter(isPaid=True).aggregate(
            total_amount=Sum('amount')
        )['total_amount'] or 0
        total_payment_count = Payment.objects.filter(isPaid=True).count()
        ten_percent_profits = Payment.objects.filter(isPaid=True).aggregate(
            profits=Sum(ExpressionWrapper(F('amount') * 0.1, output_field=DecimalField()))
        )['profits']

        data = {
            'total_payment_count': total_payment_count,
            'total_amount_received': total_amount_received,
            'ten_percent_profits': ten_percent_profits,
        }

        serializer = PaymentStatisticsSerializer(data)
        return Response(serializer.data)
    


class AdminStatisticalData(APIView):
    permission_classes  = [IsAdminUser]

    def get(self, request, *args, **kwargs):

        user_count = User.objects.count()
        therapist_count = Therapist.objects.count()
        completed_count = Booking.total_completed_bookings()
        booking_count =Booking.objects.count()
        pending_count = Booking.total_pending_bookings()
        canceled_count = Booking.total_canceled_bookings()
        payment_list = Payment.objects.order_by('-payment_date')[:5]
        data = {
            'user_count': user_count,
            'booking_count':booking_count,
            'therapist_count': therapist_count,
            'completed_count': completed_count,
            'pending_count': pending_count,
            'canceled_count': canceled_count,
        }
        payment_serializer = Payment_Booked_Serializer(payment_list,many=True)
        serializer = AdminStatisticalDataSerializer(data)
       
        return Response({
            'data': serializer.data,
            'payments_list': payment_serializer.data
        })



class CreateReportView(generics.CreateAPIView):
    queryset = TherapistReport.objects.all()
    serializer_class = ReportSerializer

class ReportListCreateView(generics.ListCreateAPIView):
    queryset = TherapistReport.objects.all()
    serializer_class = ReportTherapistList


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryBlockView(APIView):
    def put(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
            if not category.is_blocked:
                category.is_blocked = True
                category.save()
                return Response({'message': 'Category blocked successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Category is already blocked'}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


class CategoryUnblockView(APIView):
    def put(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
            if category.is_blocked:
                category.is_blocked = False
                category.save()
                return Response({'message': 'Category unblocked successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Category is not blocked'}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        



class LanguageCreateView(generics.CreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class LanguageListView(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer



class LanguageBlockView(APIView):
    def put(self, request, Language_id):
        try:
            language = Language.objects.get(pk=Language_id)
            if not language.is_blocked:
                language.is_blocked = True
                language.save()
                return Response({'message': 'language blocked successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'language is already blocked'}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'message': 'language not found'}, status=status.HTTP_404_NOT_FOUND)


class LanguageUnblockView(APIView):
    def put(self, request, Language_id):
        try:
            language = Language.objects.get(pk=Language_id)
            if language.is_blocked:
                language.is_blocked = False
                language.save()
                return Response({'message': 'language unblocked successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'language is not blocked'}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'message': 'language not found'}, status=status.HTTP_404_NOT_FOUND)
        