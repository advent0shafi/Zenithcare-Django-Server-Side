from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializers
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from zenithcare_backend import settings
from django.core.mail import send_mail,EmailMessage
from django.utils.crypto import get_random_string        
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from .models import User,OTP
from .email import send_otp_email,send_email_user
from django.utils import timezone
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth.hashers import check_password

class Register(APIView):
    def post(self, request):
        try:
            email = request.data.get('email', None)

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.save()

            response_data = {
                'user': serializer.data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except ParseError:
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response({'error': 'Validation failed', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': 'Internal server error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Home(APIView):
    def post(self, request):
        pass

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        print("its german")
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        print("failure")
        refresh = RefreshToken.for_user(user)
        access_token = str(response.data['access'])
        response.data['active'] = user.is_active
        response.data['vendor'] = user.is_therapist
        response.data['admin'] = user.is_superuser
        response.data['username'] = user.username
        response.data['id'] = user.id
        return response

class Signup(APIView):
    def post(self, request):
        try:
            email = request.data.get('email', None)
            print(email)

            try:
                serializer = UserSerializers(data=request.data)
                serializer.is_valid(raise_exception=True)
            except serializers.ValidationError as e:
                print("Serializer validation error:", e)
            
            serializer.is_valid(raise_exception=True)
            print('email  sending')
            user = serializer.save()
            print(user)
            if user is not None :
        
                otp_store = get_random_string(length=5, allowed_chars='0123456789')
                print(otp_store)
                send_otp_email(user.id,otp_store)
                otp = OTP.objects.create(user=user, otp=otp_store)
                otp.save()
            expired_otps = OTP.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(minutes=5))
            expired_otps.delete()
            response_data = {
                'user': serializer.data,
               
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        except ParseError as e:
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': 'Validation failed', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'An unknown error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class OTPVerification(APIView):
    def post(self, request):
        otp_from_user = request.data.get('otp')

        user_pk = request.data.get('id')
        users = User.objects.get(id=user_pk)
        print(users)
        otpinstance = OTP.objects.get(user=users)
        stored_otp = otpinstance.otp
        print(stored_otp,"-------------------------")
        if not otp_from_user or not user_pk or not stored_otp:
            return JsonResponse({'error': 'Invalid OTP data'}, status=400)

        if otp_from_user == stored_otp:
            try:
                user = User.objects.get(pk=user_pk)
                user.is_verified = True
                user.save()
                print("its everything okay")
                otpinstance.delete()
            except User.DoesNotExist:
                print('error User not found')
                return JsonResponse({'error': 'User not found'}, status=404)
            print('succesfull')
            return JsonResponse({'message': 'OTP verification successful'}, status=200)
        else:
            print('error ------------------in')
            return JsonResponse({'error': 'Invalid OTP'}, status=400)


class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    def get(self, request, user_id):
            
            try:
                user = User.objects.get(id=user_id)
                send_email_user.delay(user_id)
                profile_img_url = None  # Initialize to None

                if user.profile_img and user.profile_img.url:
                    profile_img_url = user.profile_img.url
            
                return Response({
                    'id': user.id,
                    'username': user.username,
                    'email':user.email,
                    'phone_number':user.phone_number,
                    'profile_img':profile_img_url,
                })
            except User.DoesNotExist:
                print('status')
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



class EditProfileView(APIView):

    def put(self, request, user_id):
        print('its here')
        try:
            
            user = User.objects.get(id=user_id)
            uploaded_file = request.FILES.get('profile_img')
            print('its entered try')
            print(uploaded_file)
            if uploaded_file:
              
                if uploaded_file.content_type.startswith('image'):
                    user.profile_img = uploaded_file
                    user.save()
                    return Response({'profile_img_url': user.profile_img.url})
                else:
                    return Response({'error': 'Invalid file format'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'No image data provided'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

class UserUpdateView(APIView):
     def put(self, request, user_id):
        user = User.objects.get(id=user_id)
        print(user)
        serializer = UserSerializers(user, data=request.data,partial=True)
       
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
           
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordUpdations(APIView):
    def put(self, request, user_id):
        try:
            old_password = request.data.get('old_password')
            new_password = request.data.get('password')
            user = User.objects.get(id=user_id)

            # Check if the old password matches the user's current password
            if not check_password(old_password, user.password):
                return Response({'message': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        



# class Signup(APIView):
#     def post(self, request):
#         try:
#             email = request.data.get('email', None)
#             print('its here vere reading')
#             if User.objects.filter(email=email).exists():
#                 print('exitsss')
#                 raise ValidationError('Email already exists.')

#             serializer = UserSerializers(data=request.data)
#             serializer.is_valid(raise_exception=True)

#             user = serializer.save()
#             print(user,'--------')
#             if user is not None :
#                 otp_store = get_random_string(length=5, allowed_chars='0123456789')
#                 print(otp_store)
#                 send_otp_email(user, otp_store)
#                 otp = OTP.objects.create(user=user, otp=otp_store)
#                 otp.save()
#             expired_otps = OTP.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(minutes=5))
#             expired_otps.delete()
#             response_data = {
#                 'user': serializer.data,
               
#             }

#             return Response(response_data, status=status.HTTP_201_CREATED)
#         except ParseError as e:
#             return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
#         except ValidationError as e:
#             return Response({'error': 'Validation failed', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response({'error': 'An unknown error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        