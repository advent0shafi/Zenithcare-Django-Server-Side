from django.shortcuts import render
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from authentification.models import User
from rest_framework import status
from django.core.exceptions import SuspiciousFileOperation
from vendor.models import Category, Language, AvailableDay, BookingSchedule, Therapist, Address
from authentification.serializers import UserSerializers
from rest_framework.generics import ListAPIView, UpdateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from django.http import JsonResponse
from rest_framework import generics
from .models import SessionMode,user_details
from .serializers import SessionModeSerializer,UserInfo
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer, BookingSessionsSerializer
from rest_framework.generics import ListAPIView
from payment.models import Payment
from django.shortcuts import get_object_or_404
from django.conf import settings
import stripe
from vendor.models import VendorWallet


class SessionModeListView(generics.ListCreateAPIView):
    serializer_class = SessionModeSerializer

    def get_queryset(self):
        return SessionMode.objects.all()


class UserVendorBooking(APIView):

    def post(request, self):

        pass


class CreateBooking(APIView):
    def post(self, request):
        # Extract data from the request
        booking_date_id = request.data.get('dataId')
        id_of_vendor = request.data.get('id')
        users = User.objects.get(id=id_of_vendor)
        therapist_data = Therapist.objects.get(user=users)
        sessions = request.data.get('sessions')
        sessions_data = SessionMode.objects.get(name=sessions)
        data = {
            'date_of_booking': request.data.get('dates'),
            # Assuming user_id is provided
            'user': request.data.get('user_id'),
            'therapist': therapist_data.id,
            'mode_of_session': sessions_data.id,
            'slot': request.data.get('dataId')
        }

        serializer = BookingSerializer(data=data)

        if serializer.is_valid():
            # Save the booking

            Bookings_dates = BookingSchedule.objects.get(id=booking_date_id)
            Bookings_dates.is_available = False
            Bookings_dates.save()
            serializer.save()

            return Response({'message': 'Booking created successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingSessionsAPIView(ListAPIView):
    serializer_class = BookingSessionsSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        return Booking.objects.filter(user=user)


class BookingUpdateAPIView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        id = self.kwargs.get('pk')
        vendor_id = self.kwargs.get('vendor_id')

        booking = Booking.objects.get(booking_id=id)
        payment = Payment.objects.get(booking=booking)
        vendor = User.objects.get(id=vendor_id)
        print(payment.payment_id, '------')
        if payment:
            stripe.api_key = settings.STRIP_SECRET_KEY
            stripe.Refund.create(
                payment_intent=payment.payment_id,
                amount=int(payment.amount),
            )
            vendor_wallet = VendorWallet.objects.get(vendor=vendor)
            vendor_wallet.reduce_balance(payment.amount)

        payment.isPaid = False
        payment.save()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingVendorSessions(ListAPIView):
    serializer_class = BookingSessionsSerializer

    def get_queryset(self):
        vendor_id = self.kwargs.get('vendor_id')
        user = get_object_or_404(User, pk=vendor_id)
        therapist = Therapist.objects.get(user=user)        
        return Booking.objects.filter(therapist=therapist).exclude(status='cancel')
    
class UserDetailView(RetrieveAPIView):
    serializer_class = UserInfo

    def get_object(self):
        booking_id = self.kwargs.get('booking_id')  # Assuming the booking_id is in the URL kwargs
        return user_details.objects.get(booking_id=booking_id)


class BookingCompleteAPIView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

