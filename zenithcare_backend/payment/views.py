from decimal import Decimal
from django.shortcuts import render
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from authentification.models import User
from rest_framework import status
from django.db.models import Sum
from django.core.exceptions import SuspiciousFileOperation
from vendor.models import Category, Language, AvailableDay, BookingSchedule, Therapist, Address
from authentification.serializers import UserSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import stripe
from django.shortcuts import redirect
from vendor_booking.models import SessionMode,Booking,user_details
from vendor_booking.serializers import BookingSerializer
from .serializers import Payment_Booked_Serializer,PaymentSerializer
from vendor.models import BookingSchedule,VendorWallet
from .models import Payment
from rest_framework.generics import ListAPIView
import json
stripe.api_key = settings.STRIP_SECRET_KEY

from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

class StripeCheckoutView(APIView):
    def post(self, request):
     
        vendorId = request.data.get("Id")
        vendor_user = User.objects.get(id=vendorId)
        therapist = Therapist.objects.get(user=vendor_user)
        datauser =json.dumps(json.loads(request.data.get('userdata'))) 
        amount = therapist.hourly_rate
        userId = request.data.get("userId")

        print(datauser,'----------------')
        print('requests strip checking',userId)
        try:
            stripe.api_key = settings.STRIP_SECRET_KEY
            pricess = int(amount* 100)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': pricess,
                            'product_data': {
                                'name':vendor_user.username,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                metadata={
                    'id':vendorId,
                    'sessions':request.data.get('sessions'),
                    'dates':request.data.get('dates'),
                    'userId':request.data.get('userId'),
                    'dataId':request.data.get('dataId'),
                    'Total_price':pricess,
                    'userdata':datauser
                },
                
                success_url=settings.SITE_URL + f'success/?success=true&session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
         
            return redirect(checkout_session.url)

        except stripe.error.StripeError as e:
            print(f"Stripe Error: {e}")
            return Response(
                {
                    'error': 'Something went wrong when creating the Stripe checkout session'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")
            return Response(
                {
                    'error': 'An error occurred while processing the request'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from django.http import JsonResponse

@csrf_exempt
def stripe_webhook_view(request):
    endpoint_secret = settings.ENDPOINT_SECRET
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        payload = request.body.decode('utf-8')
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event.data.object.id,
            expand=['line_items']
        )
        metadata = session.metadata
        vendor_id = metadata.get('id')
        user_id = metadata.get('userId')
        data_id = metadata.get('dataId')
        sessions = metadata.get('sessions')
        date = metadata.get('dates')
        userdata = metadata.get('userdata')
        data_dict = json.loads(userdata)
        name = data_dict.get('name')
        place = data_dict.get('place')
        age = data_dict.get('age')
        summary = data_dict.get('summary')
        gender = data_dict.get('gender')
        relationship_status = data_dict.get('relationship_status')
        checkout_session_id = session.payment_intent

        try:
            vendor_users = get_object_or_404(User, id=vendor_id)
            users = get_object_or_404(User, id=user_id)
            booking_slot = get_object_or_404(BookingSchedule, id=data_id)
            therapist_data = get_object_or_404(Therapist, user=vendor_users)
            amount = therapist_data.hourly_rate
            sessions_mode = get_object_or_404(SessionMode, name=sessions)
            booking = Booking.objects.create(
                user=users,
                therapist=therapist_data,
                date_of_booking=date,
                mode_of_session=sessions_mode,
                slot=booking_slot,
                payment_Id=checkout_session_id
            )
        except stripe.error.InvalidRequestError:
            return JsonResponse({'message': 'Invalid Request'}, status=400)
        
        if booking:
            # Calculate 10% deduction
            deduction = Decimal('0.10') * amount
            final_amount = amount - deduction

            # Update the vendor's wallet
            vendor_wallet, created = VendorWallet.objects.get_or_create(vendor=vendor_users)
            vendor_wallet.balance += final_amount
            vendor_wallet.save()

            # Update the payment with the final amount
            payment = Payment.objects.create(
                user=users,
                vendor_user=vendor_users,
                booking=booking,
                payment_id=checkout_session_id,
                amount=final_amount,
                  real_amount=amount,  # Deducted amount
                isPaid=True
            )
            
            if payment:
                # Create user_info object
                user_info = user_details.objects.create(
                    user_profile=users,
                    booking_id=booking,
                    name=name,
                    mobile_number=users.phone_number,
                    place=place,
                    age=age,
                    summary=summary,
                    gender=gender,
                    relationship_status=relationship_status
                )

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=200)



class PaymentHistory(ListAPIView):
    serializer_class = Payment_Booked_Serializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)  # Assuming you have a User model
        return Payment.objects.filter(user=user)

class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = Payment_Booked_Serializer


class VendorPaymentsView(APIView):
    def get(self, request, vendor_id):

        users = User.objects.get(id=vendor_id)
        print(users)
        payments = Payment.objects.filter(vendor_user=users).exclude(isPaid=False)
        print(payments)
        total_amount_received = payments.aggregate(total_amount=Sum('amount'))['total_amount'] or Decimal('0.0')

        if total_amount_received is None:
            total_amount_received = 0.0

        serializer = Payment_Booked_Serializer(payments, many=True)

        return Response({
            'total_amount_received': total_amount_received,
            'payments': serializer.data
        })

