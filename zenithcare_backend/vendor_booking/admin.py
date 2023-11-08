from django.contrib import admin
from .models import SessionMode,Booking,user_details
# Register your models here.
admin.site.register(SessionMode)

admin.site.register(Booking)
admin.site.register(user_details)
