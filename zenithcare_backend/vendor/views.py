from rest_framework.exceptions import ValidationError
from django.forms import ValidationError
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from authentification.models import User
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework import status
from django.core.exceptions import SuspiciousFileOperation
from vendor.models import Category, Language, AvailableDay, BookingSchedule, Therapist, Address, VendorWallet, Transaction
from .serializers import TherapistRegistrationSerializer, AddressSerializer, BookingScheduleSerializer, VendorWalletSerializer, VendorWalletExtraFieldsSerializer, TransactionSerializer
from authentification.serializers import UserSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from django.http import JsonResponse
from rest_framework import generics


from rest_framework.serializers import Serializer
from .serializers import TherapistSerializer  # Import the TherapistSerializer


class DetailFormView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.profile_img:
                profile_img_url = user.profile_img.url
            else:
                profile_img_url = None
            catogery = Category.objects.all()
            language = Language.objects.all()
            # Serialize the Therapist object

            return Response({
                'catogery': catogery.values('id', 'name'),
                'language': language.values('id', 'language'),
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_img': profile_img_url,
            })

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except SuspiciousFileOperation:
            return Response({'error': 'Invalid file operation'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.profile_img:
                profile_img_url = user.profile_img.url
            else:
                profile_img_url = None

            therapists = Therapist.objects.get(user=user)

            therapist_serializer = TherapistSerializer(
                therapists, context={'request': request})

            return Response({

                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone_number':user.phone_number,
                'profile_img': profile_img_url,
                'therapist': therapist_serializer.data  # Include serialized Therapist data
            })

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except SuspiciousFileOperation:
            return Response({'error': 'Invalid file operation'}, status=status.HTTP_400_BAD_REQUEST)


class TherapistAddView(APIView):
    parser_classes = [MultiPartParser]

    def get_object(self, user_id):
        therapist = get_object_or_404(Therapist, user=user_id)
        return therapist

    def post(self, request):
        user_id = request.data.get('username')
        certifications_file = request.data.get('certifications')
        print(request.data)

        # Split the 'languages' field and convert values to integers
        languages_str = request.data.get('languages')
        # Split the string into a list of IDs
        languages = languages_str.split(',')

        try:
            languages = [int(lang_id) for lang_id in languages]
        except ValueError:
            print('Invalid language IDs')
            return Response("Invalid language IDs", status=status.HTTP_400_BAD_REQUEST)

        try:
            address_building = request.data.get('address.building', '')
            address_street = request.data.get('address.street', '')
            address_district = request.data.get('address.district', '')
            address_state = request.data.get('address.state', '')
            address_zipcode = request.data.get('address.zipcode', '')
        except Exception as e:
            print("Error accessing address_data properties:", str(e))

        address_data = {
            'building': address_building,
            'street': address_street,
            'district': address_district,
            'state': address_state,
            'zipcode': address_zipcode,
        }

        # You can use your existing serializer for Address if available.
        address_serializer = AddressSerializer(data=address_data)
        if address_serializer.is_valid():
            address = address_serializer.save()
        else:
            print(address_serializer.errors)
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_instance = get_object_or_404(User, id=user_id)
        catogery_id = request.data.get('categories')
        catogery_instance = Category.objects.get(id=catogery_id)
        is_certified = request.data.get('isCertified', '').lower() == 'true'

        # Create or update the therapist instance
        therapist_data = {
            'user': user_instance,
            'bio': request.data.get('bio'),
            'certifications': certifications_file,
            'categories': catogery_instance,
            'degree': request.data.get('degree'),
            'university': request.data.get('university'),
            'experience_years': request.data.get('experience_years'),
            'hourly_rate': request.data.get('hourly_rate'),
            'address': address,
            'is_certified': is_certified  # Use 'isCertified' as is in the request
        }
        therapist, created = Therapist.objects.update_or_create(
            user=user_instance, defaults=therapist_data)
        therapist.languages.set(languages)

        if not created:
            return Response("Therapist updated successfully.", status=status.HTTP_200_OK)
        else:
            return Response("Therapist added successfully.", status=status.HTTP_201_CREATED)

    def put(self, request):
        user_id = request.data.get('username')
        therapist = self.get_object(user_id)
        certifications_file = request.data.get('certifications')

        try:
            address_building = request.data.get('address.building', [])
            address_street = request.data.get('address.street', [])
            address_district = request.data.get('address.district', [])
            address_state = request.data.get('address.state', [])
            address_zipcode = request.data.get('address.zipcode', [])
        except Exception as e:
            print("Error accessing address_data properties:", str(e))

        address_data = {
            'building': address_building,
            'street': address_street,
            'district': address_district,
            'state': address_state,
            'zipcode': address_zipcode,
        }
        address_serializer = AddressSerializer(data=address_data)
        if address_serializer.is_valid():
            address = address_serializer.save()
        else:
            print(address_serializer.errors)
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        request_data = request.data.copy()
        request_data['user'] = user_id
        request_data['address'] = address.id

        therapist_serializer = TherapistRegistrationSerializer(
            therapist, data=request_data)
        if therapist_serializer.is_valid():
            therapist = therapist_serializer.save()
            therapist.certifications = certifications_file
            therapist.save()
            return Response(therapist_serializer.data, status=status.HTTP_200_OK)
        else:
            address.delete()
            print(therapist_serializer.errors)
            return Response(therapist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class topTherapist(APIView):
    def get(request, self):
        therapists = Therapist.objects.all()
        serializer = TherapistSerializer(therapists, many=True)

        return Response(serializer.data)


class CreateSlot(APIView):
    def post(self, request, user_id):
       
        date = request.data.get('date')
        time = request.data.get('time')

        try:
            BookingSchedule.delete_expired_slots()
            user = User.objects.get(id=user_id)
            therapist = Therapist.objects.get(user=user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Therapist.DoesNotExist:
            return Response({'error': 'Therapist not found'}, status=status.HTTP_404_NOT_FOUND)

        if not date or not time:
            return Response({'error': 'Date and time are required'}, status=status.HTTP_400_BAD_REQUEST)

        booking_schedule = BookingSchedule.objects.create(
            therapist=therapist,
            date=date,
            time=time,
            is_available=True  
        )

        serializer = BookingScheduleSerializer(booking_schedule)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            therapist = Therapist.objects.get(user=user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Therapist.DoesNotExist:
            return Response({'error': 'Therapist not found'}, status=status.HTTP_404_NOT_FOUND)

        slotlist = BookingSchedule.objects.filter(
            therapist=therapist, is_available=True)
        serlizers = BookingScheduleSerializer(slotlist, many=True)
        data = {'userdata': serlizers.data}
        return Response(data)


class DeleteSlot(APIView):
    def delete(self, request, slot_id):
        try:
            slot = BookingSchedule.objects.get(id=slot_id)
            slot.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BookingSchedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingScheduleListView(ListAPIView):
    serializer_class = BookingScheduleSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        therapist = get_object_or_404(Therapist, user=user)
        return BookingSchedule.objects.filter(therapist=therapist)


class VendorWalletAPIView(RetrieveAPIView):
    queryset = VendorWallet.objects.all()
    serializer_class = VendorWalletSerializer
    lookup_field = 'vendor_id'

    def get_object(self):
        vendor_id = self.kwargs.get(self.lookup_field)
        try:
            return VendorWallet.objects.get(vendor_id=vendor_id)
        except VendorWallet.DoesNotExist:
            vendor = User.objects.get(id=vendor_id)
            wallet = VendorWallet.objects.create(vendor=vendor, balance=0)
            return wallet


class VendorWalletListAPIView(ListAPIView):
    serializer_class = VendorWalletExtraFieldsSerializer

    def get_queryset(self):
        return VendorWallet.objects.filter(balance__gt=0)


class PayAmountView(UpdateAPIView):
    serializer_class = VendorWalletExtraFieldsSerializer

    def update(self, request, *args, **kwargs):
        vendor_id = self.kwargs.get('vendor_id')
        instance = VendorWallet.objects.get(vendor=vendor_id)
        amount = request.data.get('amount')
        description = request.data.get('description')
        try:
            instance.pay_amount(amount, description)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_BAD_REQUEST)


class TransactionListByVendorView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        return Transaction.objects.filter(user__id=vendor_id)
