from rest_framework import serializers
from .models import Therapist, Address, Category, Language, AvailableDay, BookingSchedule,Transaction

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class AvailableDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDay
        fields = '__all__'

class BookingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSchedule
        fields = '__all__'

class TherapistSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    therapist_name = serializers.CharField(source='user.username')
    therapist_image = serializers.CharField(source='user.profile_img')
    categories = CategorySerializer()  # Adjusted here
    languages = LanguageSerializer(many=True)  # Adjusted here
    booking_schedule = BookingScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Therapist
        fields = ('id', 'user','therapist_name','therapist_image', 'bio', 'certifications', 'categories','degree','university', 'languages', 
                  'experience_years', 'hourly_rate', 'address', 'booking_schedule', 'is_certified')
from rest_framework import serializers

from rest_framework import serializers

class TherapistRegistrationSerializer(serializers.ModelSerializer):
    languages = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Therapist
        fields = ('user', 'bio', 'certifications', 'categories', 'languages',
                  'experience_years', 'hourly_rate', 'address', 'is_certified')

    
from .models import VendorWallet

class VendorWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorWallet
        fields = '__all__'

class VendorWalletExtraFieldsSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.username')
    vendor_image = serializers.CharField(source='vendor.profile_img')
    class Meta:
        model = VendorWallet
        fields = ['vendor','vendor_name','vendor_image','id','balance']



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'