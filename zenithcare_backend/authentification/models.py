from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group

from django.db import models
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    profile_img = models.ImageField(upload_to='profile', blank=True, null=True)
    is_therapist = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True,)
    roles = models.CharField(max_length=15, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    groups = models.ManyToManyField(Group, related_name='custom_user')

    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=5)
    created_at = models.DateTimeField(default=timezone.now)
    def is_expired(self):
        # Define your desired time period (e.g., 5 minutes)
        expiration_time = timezone.timedelta(minutes=5)
        return timezone.now() > (self.created_at + expiration_time)