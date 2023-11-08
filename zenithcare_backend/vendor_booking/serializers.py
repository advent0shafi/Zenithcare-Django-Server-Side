from rest_framework import serializers
from .models import SessionMode ,Booking,user_details

class SessionModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionMode
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class UserInfo(serializers.ModelSerializer):
    class Meta:
        model = user_details
        fields = '__all__'


class BookingSessionsSerializer(serializers.ModelSerializer):
    therapist_img = serializers.CharField(source='therapist.user.profile_img')
    therapist_name = serializers.CharField(source='therapist.user.username')
    user_name = serializers.CharField(source='user.username')
    user_img = serializers.CharField(source='user.profile_img')
    therapist_amount = serializers.CharField(source='therapist.hourly_rate')
    therapist_id = serializers.CharField(source='therapist.user.id')
    time = serializers.CharField(source='slot.time')
    mode_of_session = serializers.CharField(source='mode_of_session.name')
    class Meta:
        model = Booking
        fields = ['booking_id','user_name','user_img','therapist_amount','therapist_name','date_of_booking','status','payment_type','payment_Id','mode_of_session','therapist_img','time','therapist_id']



