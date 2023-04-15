from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import FeedbackSerializer,StatsSerializer,ProfileSerializer
from .models import Feedback,Stats,Profile
from rest_framework.response import Response 
from rest_framework import status
from LoginReg.models import User
from user.models import Notifications
from joblib import load

# load model and vectorizer
model = load('model.joblib')
cv = load('cv.joblib')
# Create your views here.

#for profile model
# class ProfileAPI(APIView):
#     def get(self,request,pk=None,format=None):
#         id=pk
#         if id is not None:
#             ngo = Profile.objects.get(id=id)
#             serializer = ProfileSerializer(ngo)
#             return Response(serializer.data)
#         ngo = Profile.objects.all()
#         serializer = ProfileSerializer(ngo,many=True)
#         return Response(serializer.data)

    
#     def post(self,request,format=None):
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'Data Created'})
#         return Response(serializer.errors)

    
#     def patch(self,request,pk,format=None):
#         id=pk
#         ngo=Profile.objects.get(id=id)
#         serializer = ProfileSerializer(ngo, data=request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'Partial data updated'})
#         return Response(serializer.errors)

#     def delete(self,request,pk,format=None):
#         ngo = Profile.objects.get(id=pk)
#         ngo.delete()
#         return Response({'msg':'Data Deleted'})  

class UserProfileView(APIView):
    def get(self,request,username=None,format=None):
        if username is not None:
            profile = Profile.objects.get(username=username)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile,many=True)
        return Response(serializer.data)

    
    def post(self,request,format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'})
        return Response(serializer.errors)

    
    def patch(self,request,username,format=None):
        username=username
        profile=Profile.objects.get(username=username)
        serializer = ProfileSerializer(profile, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial data updated'})
        return Response(serializer.errors)

    def delete(self,request,username,format=None):
        profile = Profile.objects.get(username=username)
        profile.delete()
        return Response({'msg':'Data Deleted'})    


#for stats model
class StatsAPI(APIView):
    def get(self,request,pk=None,format=None):
        id=pk
        if id is not None:
            ngo = Stats.objects.get(id=id)
            serializer = StatsSerializer(ngo)
            return Response(serializer.data)
        ngo = Stats.objects.all()
        serializer = StatsSerializer(ngo,many=True)
        return Response(serializer.data)

    
    def post(self,request,format=None):
        serializer = StatsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'})
        return Response(serializer.errors)

    
    def patch(self,request,pk,format=None):
        id=pk
        ngo=Stats.objects.get(id=id)
        serializer = StatsSerializer(ngo, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial data updated'})
        return Response(serializer.errors)

    def delete(self,request,pk,format=None):
        ngo = Stats.objects.get(id=pk)
        ngo.delete()
        return Response({'msg':'Data Deleted'})


#for feedback model
# class FeedbackAPI(APIView):
#     def get(self,request,pk=None,format=None):
#         id=pk
#         if id is not None:
#             ngo = Feedback.objects.get(id=id)
#             serializer = FeedbackSerializer(ngo)
#             return Response(serializer.data)
#         ngo = Feedback.objects.all()
#         serializer = FeedbackSerializer(ngo,many=True)
#         return Response(serializer.data)

    
#     def post(self,request,format=None):
#         serializer = FeedbackSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'Data Created'})
#         return Response(serializer.errors)

#     def delete(self,request,pk,format=None):
#         ngo = Feedback.objects.get(id=pk)
#         ngo.delete()
#         return Response({'msg':'Data Deleted'})

class FeedbackAPIView(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            # Get the user object by username
            user = User.objects.get(username=feedback.name)
            # Create a notification object
            notification = Notifications.objects.create(
                user=user,
                topic='New Feedback',
                content=[f'hey']
            )
            content=["the food was bad"]
            result = model.predict(cv.transform(content))
            if(result==0):
                print("Postive Response")
            else:
                print("Negative Response")
            notification.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk=None,format=None):
        id=pk
        if id is not None:
            ngo = Feedback.objects.get(id=id)
            serializer = FeedbackSerializer(ngo)
            return Response(serializer.data)
        ngo = Feedback.objects.all()
        serializer = FeedbackSerializer(ngo,many=True)
        return Response(serializer.data)

def FBAnalysis(request):
    content=["the food was bad"]
    result = model.predict(cv.transform(content))
    if(result==1):
        print("Postive Response")
    else:
        print("Negative Response")



