# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
      path('create/',views.MessageCreateView.as_view(),name='message-create'),
    path('vendor-details/<int:vendor_id>/', views.VendorDetailsView.as_view(), name='vendor-details'),

    path('chat/<int:user_id>/<int:vendor_id>/', views.UserAuthorChatView.as_view(), name='user-doctor-chat'),
    path('vendor-chat/<int:vendor_id>/', views.VendorChatView.as_view(), name='vendor-chat'),

]