from rest_framework import serializers
from .models import TherapistReport

class AdminStatisticalDataSerializer(serializers.Serializer):
    user_count = serializers.IntegerField()
    booking_count =serializers.IntegerField()
    therapist_count = serializers.IntegerField()
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()
    canceled_count = serializers.IntegerField()


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapistReport
        fields = '__all__'



class ReportTherapistList(serializers.ModelSerializer):
     therapist_name = serializers.CharField(source='therapist.username')
     user_name = serializers.CharField(source='reported_by.username')
     therapist_image = serializers.CharField(source='therapist.profile_img')
     class Meta:
        model = TherapistReport
        fields = ['therapist_name','user_name','therapist_image','therapist','reported_by','reason','description']
