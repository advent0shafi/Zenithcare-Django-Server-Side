from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
   
    path('home',Home.as_view()),
    path('signup',Signup.as_view(),name='Signup'),
    path('logout ', LogoutView.as_view(), name ='logout'),
    path('otp',OTPVerification.as_view()),
    path('user/<int:user_id>/',UserProfile.as_view()),
    path('image/<int:user_id>/',EditProfileView.as_view()),
    path('register',Register.as_view()),
    path('password/<int:user_id>/',PasswordUpdations.as_view(),name='password'),
    path('update/<int:user_id>/', UserUpdateView.as_view(), name='user-update'),

]
