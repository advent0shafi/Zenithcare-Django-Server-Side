from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class Payment_Booked_Serializer(serializers.ModelSerializer):
    booked_id = serializers.CharField(source='booking.booking_id')
    user = serializers.CharField(source='user.username')
    vendor_user = serializers.CharField(source='vendor_user.username')
    booked_date = serializers.CharField(source='booking.date_of_booking')
    booked_slote = serializers.CharField(source='booking.slot.time')
    class Meta:
        model = Payment
        fields =['payment_id','amount','isPaid','real_amount','payment_date','user','booked_id','booked_date','booked_slote','vendor_user']

    
class PaymentStatisticsSerializer(serializers.Serializer):
    total_payment_count = serializers.IntegerField()
    total_amount_received = serializers.DecimalField(max_digits=10, decimal_places=2)
    ten_percent_profits = serializers.DecimalField(max_digits=10, decimal_places=2)
