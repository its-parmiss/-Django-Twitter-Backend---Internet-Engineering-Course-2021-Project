from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  
from rest_framework.parsers import JSONParser
from .models import Tweet,UserFollowing,Account
from .serializers import TweetSerializer,UserFollowingSerializer,LikeSerializer
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer,LikeSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class=TweetSerializer
    queryset=Tweet.objects.all()
    lookup_field = 'pk'
    def get(self,request,pk = None):
        if(pk):
            return self.retrieve(request)
        else:
            return self.list(request)
    def post(self,request):
        request_data = {}
        request_data['text']=request.data.get("text")
        request_data['user_id']=request.user.id
        request_data['likes']=[]
        # request_data['parent']=request.data.get("parent")
        request_data['parent']=None
        # tweet = Tweet('text'=request.data.get("text"),'user_id'=,)
        serializers=TweetSerializer(data=request_data)
        if serializers.is_valid():
            serializers.save()
        else:
            print("here")
            print(serializers.errors)
        return Response(serializers.data)
    def put(self,request,pk):
        return self.update(request,pk)
    def delete(self,request,pk):
        return self.destroy(request,pk)


#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
class uploadProfileImageAPI(generics.GenericAPIView):
    def post(self,request):
        user = Account.objects.get(id=request.user.id)
        thumbnail = request.FILES["image"]
        user.profile_image=thumbnail
        serializers= UserSerializer(user)
        return Response(serializers.data)
class UserAPIView(generics.GenericAPIView,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class=UserSerializer
    queryset=User.objects.all()
    def get(self,request):
        user = Account.objects.get(id=request.user.id)
        serializers= UserSerializer(user)
        return Response(serializers.data) 
    def put(self,request):
        
        serializers = UserSerializer(data=request.data)
        # return self.update(request)
        if serializers.is_valid():
            user=serializers.save()
        return Response(serializers.data,status.HTTP_201_CREATED)
           
        return Response(serializers.data,status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        user=Account.objects.get(id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)              
class FollowAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=UserFollowingSerializer   
    def post(self,request):
        request_data = {}
        request_data['following_user_id']=request.data.get("following_user_id")
        request_data['user_id']=request.user.id
        serializers=UserFollowingSerializer(data=request_data)
        if serializers.is_valid():
            serializers.save()
        return Response(serializers.data)
class LikeAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=LikeSerializer   
    def post(self,request,pk):
        request_data = {}
        request_data['user_id']=request.user.id
        request_data['tweet_id']=pk
        serializers=LikeSerializer(data=request_data)
        if serializers.is_valid():
            serializers.save()
        return Response(serializers.data)

# class TweetAPIView(APIView):
#     def get(self,request):
#         tweets= Tweet.objects.all()
#         serializers=TweetSerializer(tweets,many=True)
#         return Response(serializers.data)               

#     def post(self,request):
#         serializers = TweetSerializer(data=request.data)

#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data,status.HTTP_201_CREATED)
           
#         return Response(serializers.data,status.HTTP_400_BAD_REQUEST)

# class TweetDetails(APIView):
#     def get_object(self,pk):
#         try:
#             tweet=Tweet.objects.get(pk=pk)
#             return tweet
#         except Tweet.DoesNotExist:
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)      
#     def get(self,request, pk):
#         tweet=self.get_object(pk)
#         serializers=TweetSerializer(tweet)
#         return Response(serializers.data)
#     def put(self,request, pk):
#         tweet=self.get_object(pk)
#         serializers = TweetSerializer(tweet,data=request.data)

#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk):
#         tweet=self.get_object(pk)
#         tweet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# # @api_view(['GET','PUT','DELETE'])
# # def tweetdetails(request,pk):
    
# #     try:
# #         tweet=Tweet.objects.get(pk=pk)

# #     except Tweet.DoesNotExist:
# #         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
# #     if request.method =='GET':
# #         serializers=TweetSerializer(tweet)
# #         return Response(serializers.data)
# #     elif request.method =='PUT':
# #         serializers = TweetSerializer(tweet,data=request.data)

# #         if serializers.is_valid():
# #             serializers.save()
# #             return Response(serializers.data)
# #         return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
# #     elif request.method =='DELETE':
# #         tweet.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
# # # Create your views here.
