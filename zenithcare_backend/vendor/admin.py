from django.contrib import admin
from .models import Therapist, Address, Category, Language, AvailableDay, BookingSchedule,VendorWallet,Transaction

class BookingScheduleInline(admin.TabularInline):
    model = BookingSchedule

class TherapistAdmin(admin.ModelAdmin):
    inlines = [BookingScheduleInline,]  # Include BookingSchedule as inline

admin.site.register(BookingSchedule)
admin.site.register(Address)

admin.site.register(Category)
admin.site.register(Language)
admin.site.register(AvailableDay)
admin.site.register(Therapist, TherapistAdmin)
admin.site.register(VendorWallet)

admin.site.register(Transaction)
