from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [ 
  path('create-checkout-session',StripeCheckoutView.as_view(), name='payment'),
path('webhook',stripe_webhook_view),
path('payment_history/<int:user_id>/',PaymentHistory.as_view(), name='booking-sessions'),
path('payment-list',PaymentListView.as_view()),
 path('vendor-payments/<int:vendor_id>/', VendorPaymentsView.as_view(), name='vendor_payments'),
 
]
