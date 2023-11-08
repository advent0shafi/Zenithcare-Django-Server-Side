from django.db import models
from vendor_booking.models import Booking
from authentification.models import User
# Create your models here.
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_payments')
    vendor_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='vendor_payments')
    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    real_amount = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    isPaid = models.BooleanField(default=True)
    payment_date = models.DateTimeField(auto_now_add=True)


