from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from uuid import uuid4
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.models import Site
from rest_framework.mixins import ListModelMixin,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin
from .customerpermissions import IsVerified
from django.contrib.auth import logout
from rest_framework import status

# Create your views here.
class RegistrationAPI(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({'status':422, 'errors': serializer.errors, 'message': 'Unprocessable Entity'})

        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user.save() 
        return Response({'status': 200, 'payload' : {"User email" : user.email , "User id" : user.id},'message' : 'Registration Successful', 'refresh': str(refresh), 'access': str(refresh.access_token)})

class UserAPI(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsVerified]
    def get(self, request):
        user = request.user
        user_data = UserSerializer(user).data
        return Response({'status': 200, 'payload':user_data})

class SendVerficationAPI(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        user = request.user
        token =  uuid4()
        user.email_token = token
        user.save()
        try:
            subject = 'Welcome to Core Managment System'
            message = f'Hi!\n{user.First_name}, thank you for registering in Core Managment System.\nPlease Click here to verfy Your Account {Site.objects.get_current().domain}accounts/email-verification/{user.id}/{token}/\nThis is a Computer generated mail don\'t reply to this mail'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return Response({'status': 200,'message' : 'Please Check Your Mail, an Email verfication link has been provided'})
        except Exception as e:
            return Response({'status': 405, 'error': str(e) ,'message': 'Sorry Some error has occured, Please try again after sometime'})

class ValidateVerificationView(APIView):
    def get(self, request, id, token):
        try:
            user = User.objects.get(id = id)
            if(token == user.email_token):
                user.is_email_verified = True
                user.save()
                return HttpResponse('<h1>User is Verified Successfully</h1>')
            else:
                return HttpResponse('<h1>Token is not valid</h1>')
        except:
            return HttpResponse('<h1>Sorry Some error has occured</h1>')

class UserLogout(APIView):
    def get(self,request,id):
        try:
            user = User.objects.get(id = id)
            request.user.auth_token.delete()
            logout(request)

            return Response('User Logged out successfully')
        except Exception as e:
            return Response({'status': 405, 'error': str(e) ,'message': 'Sorry Some error has occured, Please try again after sometime'})

class UserDetailAPIView(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get(self, request, username):
        user = self.get_object(username)
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, username):
        user = self.get_object(username)
        if user is not None:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
