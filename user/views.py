from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from uuid import uuid4
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer,NotificationsSerializer,DonationSerializer,VolunteerSerializer,CommunitySerializer
from rest_framework import status
from rest_framework import generics
from .models import Donation,Volunteer,Notifications,Profile,Community
from django.db.models import Count
from django.db.models import Sum
from LoginReg.models import User
from rest_framework.parsers import MultiPartParser, FormParser
import datetime
import pytz
import time


# Create your views here.

# class UserNotificationView(APIView):
#     def get(self, request, username):
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#         notifications = Notifications.objects.filter(user=user)
#         serializer = NotificationsSerializer(notifications, many=True)
#         return Response(serializer.data)

class CreateNotificationTimeView(generics.CreateAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    default_post_time = '09:00:00'  # Default post time in UTC

    def post(self, request, *args, **kwargs):
        # Parse the default post time string into a datetime object
        post_time = datetime.datetime.strptime(self.default_post_time, '%H:%M:%S')

        # Get the current time in UTC
        now = datetime.datetime.now(pytz.utc)

        # Calculate the delay time in seconds
        delay_time = (post_time - now.time()).seconds

        # Sleep for the delay time
        if delay_time > 0:
            time.sleep(delay_time)

        # Create the notification
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Return the response
        return Response(serializer.data, status=201, headers=headers)
    
class CreateNotificationView(generics.CreateAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class ListNotificationView(generics.ListAPIView):
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if username:
            return Notifications.objects.filter(user__username=username)
        else:
            return Notifications.objects.all()
        
class ListAllNotificationView(generics.ListAPIView):
    serializer_class = NotificationsSerializer
    queryset = Notifications.objects.all()


class NgoDonationStats(APIView):
    def get(self, request, ngo, format=None):
        ngo_donations = Donation.objects.filter(ngo=ngo).values('cooked_food').annotate(total_quantity=Sum('quantity'))
        data = [{'cooked_food': donation['cooked_food'], 'total_quantity': donation['total_quantity']} for donation in ngo_donations]
        return Response(data)
   
class DonationListCreateView(generics.ListCreateAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        queryset = Donation.objects.all()

        # Group donations by NGO
        if 'group_by_ngo' in self.request.query_params:
            queryset = queryset.values('ngo').annotate(
                total_donation=Count('id'),
            ).order_by('ngo')
        else:
            queryset = queryset.order_by('-date_time')

        return queryset
    
class DonationBy(APIView):
    def get(self, request):
        donations = Donation.objects.values('ngo', 'user__username', 'quantity')
        donations_by_ngo = {}
        for donation in donations:
            ngo = donation['ngo']
            username = donation['user__username']
            quantity = donation['quantity']
            if ngo not in donations_by_ngo:
                donations_by_ngo[ngo] = {}
            if username not in donations_by_ngo[ngo]:
                donations_by_ngo[ngo][username] = 0
            donations_by_ngo[ngo][username] += quantity
        return Response(donations_by_ngo)
    
class DonationLeaderboard(APIView):
    def get(self, request):
        donations = Donation.objects.values('user__username').annotate(total_donations=Sum('quantity')).order_by('-total_donations')
        leaderboard = [{'username': donation['user__username'], 'total_donations': donation['total_donations']} for donation in donations]
        return Response(leaderboard)
    
# class VolunteerListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = VolunteerSerializer

#     def get_queryset(self):
#         queryset = Volunteer.objects.annotate(
#             volunteer_count=Count('ngo')
#         ).order_by('ngo')

#         # Group volunteers of the same NGO together
#         if 'group_by_ngo' in self.request.query_params:
#             queryset = queryset.filter(
#                 volunteer_count__gt=1
#             )

#         return queryset

class VolunteerListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = VolunteerSerializer

    def perform_create(self, serializer):
        volunteer = serializer.save()
        ngo = serializer.data['ngo']
        # Retrieve the email address of the NGO related to the volunteer from the User model
        try:
            user = User.objects.get(username=ngo)
            ngo_email = user.email
        except User.DoesNotExist:
            # If no matching User object is found, use a default email address
            ngo_email = 'rishj113@gmail.com'

        # Send an email to the NGO related to the volunteer
        message = f"New volunteer: {volunteer.First_name} {volunteer.Last_name} has joined your NGO"
        send_mail(
            subject='New volunteer registration',
            message=message,
            from_email='muchhaladeepika@gmail.com',  # Change 'example.com' to your email domain
            recipient_list=[ngo_email],
            fail_silently=False,
        )

        # Create a notification for the user related to the volunteer
        if serializer.is_valid():
            notification = Notifications.objects.create(
                topic='New Volunteer Registration',
                content=f'A new volunteer named {volunteer.First_name} has registered with your NGO.'
            )
            notification.save()




class UserProfileView(APIView):
    def get(self,request,username=None,format=None):
        username=username
        if id is not None:
            profile = Profile.objects.get(username=username)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        profile = Profile.objects.all()
        serializer = UserProfileSerializer(profile,many=True)
        return Response(serializer.data)

    
    def post(self,request,format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'})
        return Response(serializer.errors)

    
    def patch(self,request,username,format=None):
        username=username
        profile=Profile.objects.get(username=username)
        serializer = UserProfileSerializer(profile, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial data updated'})
        return Response(serializer.errors)

    def delete(self,request,username,format=None):
        profile = Profile.objects.get(username=username)
        profile.delete()
        return Response({'msg':'Data Deleted'})   
    
class CommunityPosts(APIView):
    def post(self, request):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            posts=serializer.save()
            serializer.save()
            notification = Notifications.objects.create(
            topic='New Post',
            content=f'{posts.username} has just posted on Community.'
            )
            notification.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = Community.objects.all()
        serializer = CommunitySerializer(posts, many=True)
        return Response(serializer.data)

class ContactUsView(APIView):
    def post(self, request):
        name = request.data.get('name', '')
        email = request.data.get('email', '')
        phone = request.data.get('phone', '')
        message = request.data.get('message', '')

        # Send email
        send_mail(
            'New Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}',
            email,  # Sender's email address
            ['muchhaladeepika@gmail.com'],  # Recipient email addresses
            fail_silently=False,
        )

        return Response({'message': 'Email sent successfully.'})