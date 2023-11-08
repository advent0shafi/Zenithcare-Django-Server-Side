from django.contrib import admin
from django.urls import path, include
from .views import SessionModeListView,CreateBooking,BookingSessionsAPIView,BookingUpdateAPIView,BookingVendorSessions,UserDetailView,BookingCompleteAPIView

urlpatterns = [ 
 path('session_modes/', SessionModeListView.as_view(), name='session-mode-list'),
path('create',CreateBooking.as_view()),
path('booking-sessions/<int:user_id>/', BookingSessionsAPIView.as_view(), name='booking-sessions'),
path('booking-vendor-sessions/<int:vendor_id>/', BookingVendorSessions.as_view(), name='booking-vendor-sessions'),
path('user-details/<int:booking_id>/', UserDetailView.as_view(), name='user-details-list'),
 path('bookings-update/<int:pk>/<int:vendor_id>',BookingUpdateAPIView.as_view(), name='booking-update'),
  path('bookings-complete/<int:pk>/',BookingCompleteAPIView.as_view(), name='booking-complete-update'),

]
