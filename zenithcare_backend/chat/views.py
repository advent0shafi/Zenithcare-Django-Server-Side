from django.shortcuts import render
from .serializers import MessageSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message  # Import the models module
from authentification.models import User
from django.db import models
from authentification.serializers import UserSerializers




# Create your views here.
class VendorDetailsView(APIView):
    def get(self,request,vendor_id):

        vendor = User.objects.get(id=vendor_id,is_vendor=True)
        if vendor :
            data = {
                'username':vendor.username
                    
                }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MessageCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        print(request.data)
        print("here")
        if serializer.is_valid():
            serializer.save()
            print(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAuthorChatView(APIView):
    def get(self, request, user_id, vendor_id, *args, **kwargs):
        try:
            first_user_profile = User.objects.get(id=user_id)
            vendor_profile = User.objects.get(id=vendor_id)
            print('herer',first_user_profile,vendor_profile)
        except User.DoesNotExist:
            return Response({"error": "invalid user or doctor"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all messages related to the user and doctor
        messages = Message.objects.filter(
            (models.Q(sender=first_user_profile) & models.Q(receiver=vendor_profile)) |
            (models.Q(sender=vendor_profile) & models.Q(receiver=first_user_profile))
        ).order_by('timestamp')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class VendorChatView(APIView):
#     def get(self, request, vendor_id):
#         try:
#             print("here")
#             vendor_profile = CustomUser.objects.get(id=vendor_id, is_vendor=True)  # Ensure it's a vendor
#         except CustomUser.DoesNotExist:
#             return Response({"error": "Invalid vendor"}, status=status.HTTP_400_BAD_REQUEST)

#         # Fetch all messages related to the vendor
#         messages = Message.objects.filter(
#             models.Q(receiver=vendor_profile)
#         ).order_by('timestamp')

#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class VendorChatView(APIView):
    def get(self, request, vendor_id, *args, **kwargs):
        try:
            user = User.objects.get(id=vendor_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Retrieve distinct combinations of sender and receiver IDs from Message model
        users_chatted_with = Message.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        ).exclude(sender=user).values('sender', 'receiver').distinct()

        # Extract unique user IDs from the combinations
        user_ids = set()
        for chat in users_chatted_with:
            user_ids.add(chat['sender'])
            user_ids.add(chat['receiver'])

        # Remove the current user's ID from the set
        user_ids.discard(user.id)

        # Fetch the corresponding users
        users = User.objects.filter(id__in=user_ids)

        # Serialize the list of users
        serializer = UserSerializers(users, many=True)

        return Response(serializer.data, status=200)