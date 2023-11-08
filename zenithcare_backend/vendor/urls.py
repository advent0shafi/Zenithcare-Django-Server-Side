from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
   
path('profile/<int:user_id>',ProfileView.as_view()),
path('detaitsform/<int:user_id>',DetailFormView.as_view()),
path('add-therapist/', TherapistAddView.as_view()),
path('create-slot/<int:user_id>',CreateSlot.as_view()),
path('delete_slote/<int:slot_id>',DeleteSlot.as_view()),
path('topTherapist',topTherapist.as_view()),
path('bookings/<int:user_id>/', BookingScheduleListView.as_view(), name='booking-schedule-list'),
path('vendor-wallet/<int:vendor_id>/', VendorWalletAPIView.as_view(), name='booking-modal-list'),
path('vendorwallets/', VendorWalletListAPIView.as_view(), name='vendor-wallet-list'),
path('pay-amount/<int:vendor_id>/', PayAmountView.as_view(), name='pay-amount'),
path('transactions/<int:vendor_id>/',TransactionListByVendorView.as_view(), name='transaction-list-by-vendor'),
]
