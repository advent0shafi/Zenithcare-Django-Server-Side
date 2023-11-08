from django.db import models
from authentification.models import User
from django.utils import timezone
from decimal import Decimal 
from django.utils import timezone
from django.core.exceptions import ValidationError


class Address(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
   
    def __str__(self):
        return f"{self.building}, {self.street}, {self.district}, {self.state}"
class Specilizations(models.Model):
    specilizations = models.CharField(max_length=100)

    def __str__(self):
        return self.specilizations

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_blocked = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Language(models.Model):
    language = models.CharField(max_length=100)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.language

class AvailableDay(models.Model):
    day = models.CharField(max_length=15)  # Store day abbreviation, e.g., "Mon", "Tue", etc.

    def __str__(self):
        return self.day

class BookingSchedule(models.Model):
    therapist = models.ForeignKey('Therapist', on_delete=models.CASCADE)
    available_day = models.ForeignKey(AvailableDay,null=True,blank=True, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    time = models.CharField(max_length=8,null=True,blank=True, choices=[("10 AM", "10 AM"), ("10:20AM", "10:20AM"),
                                                  ("11:40AM", "11:40 AM"), ("12:00 PM", "12:00 PM"),
                                                  ("12:20 PM", "12:20 PM"), ("2:40 PM", "2:40 PM"),
                                                  ("3 PM", "3 PM"), ("3:20 PM", "3:20 PM"),
                                                  ("3:40 PM", "3:40 PM"), ("4:00 PM", "4:00 PM")])
    is_available = models.BooleanField(default=True)
    @classmethod
    def delete_expired_slots(cls):
        now = timezone.now()
        expired_slots = cls.objects.filter(
            date__lt=now.date(),
            time__lt=now.time(),
            is_available=True
        )
        expired_slots.delete()
    
    def __str__(self):
        return f"{self.id}-{self.therapist} - {self.date} {self.time} (Available: {self.is_available})"
  
    class Meta:
        unique_together = ['therapist', 'date', 'time']

class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    certifications = models.FileField(upload_to='certification_files/')
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    specilizations  =models.ForeignKey(Specilizations,on_delete=models.CASCADE,blank=True,null=True)
    languages = models.ManyToManyField(Language) 
    degree = models.CharField(max_length=255,blank=True,null=True)
    university = models.CharField(max_length=255,blank=True,null=True)
    experience_years = models.PositiveIntegerField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_certified = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)



class VendorWallet(models.Model):
    vendor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    
    def pay_amount(self, amount, description):
        amount = Decimal(amount)
        
        # Check if the amount is positive
        if amount <= 0:
            raise ValueError("Amount must be a positive number")
        
        if self.balance >= amount:
            self.balance -= amount
            self.save()

            Transaction.objects.create(user=self.vendor, amount=amount, description=description)
        else:
            raise ValueError("Insufficient balance")

    def reduce_balance(self, amount):
        amount = Decimal(amount)
        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValidationError("Insufficient balance")

