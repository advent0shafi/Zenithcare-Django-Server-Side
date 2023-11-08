from django.db import models
from authentification.models import User
from vendor.models import Therapist,BookingSchedule


class SessionMode(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancel', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('online', 'Online Payment'),
        ('wallet', 'Wallet'),
    ]

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    mode_of_session = models.ForeignKey(SessionMode, on_delete=models.CASCADE)
    slot = models.ForeignKey(BookingSchedule, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES,default='online')
    payment_Id = models.CharField(max_length=100,null=True,blank=True, unique=True)

    @classmethod
    def total_completed_bookings(cls):
        return cls.objects.filter(status='completed').count()

    @classmethod
    def total_pending_bookings(cls):
        return cls.objects.filter(status='pending').count()

    @classmethod
    def total_canceled_bookings(cls):
        return cls.objects.filter(status='cancel').count()
    
    def __str__(self):
        return f"Booking {self.booking_id}"
    


class user_details(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_profile')
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booked_Details')
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    place = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    summary =  models.TextField(blank=True,null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')

    RELATIONSHIP_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('In a Relationship', 'In a Relationship'),
    ]
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='Single')

    def __str__(self):
        return self.name