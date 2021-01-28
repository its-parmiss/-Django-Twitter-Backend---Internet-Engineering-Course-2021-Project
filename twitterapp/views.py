from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Tweet, UserFollowing, Account, Image, Hashtag
from .serializers import TweetSerializer, UserFollowingSerializer, LikeSerializer, HashtagSerializer
from .models import Tweet, UserFollowing, Account,Image,Hashtag
from .serializers import TweetSerializer, UserFollowingSerializer, LikeSerializer,HashtagSerializer,TweetListSerializer
from .functions import extract_hashtags
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
# from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, LikeSerializer, ImageSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
import json


class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    lookup_field = 'pk'

    def get(self, request, pk=None):
        if (pk):
            return self.retrieve(request)
        else:
            user=Account.objects.get(id=request.user.id)
            serializer=UserSerializer(user)
            for following in serializer.data['following']:
                dict=[]
                fid=following['following_user_id']
                fuser=Account.objects.get(id=fid)
                fserializer=UserSerializer(fuser)
                for tweet in fserializer.data['tweets']:
                    dict.append(tweet)
            return JsonResponse(dict,safe=False)
    def post(self, request):
        request_data = {}
        text = request.data.get("text")
        hashtags = extract_hashtags(text)
        hashkey = None
        if (hashtags):
            for hashtag in hashtags:
                try:
                    hashobj = Hashtag.objects.get(key=hashtag)
                    hashkey = hashobj.id
                except Hashtag.DoesNotExist:
                    hashobj = None

                if (hashobj):
                    hasshkey = hashobj.id
                else:
                    hashobj = Hashtag.objects.create(key=hashtag)
                    hashkey = hashobj.id
                    print(hashtag)
                    print(hashkey)
        request_data['hashtag'] = hashkey
        request_data['text'] = text
        request_data['user'] = request.user.id
        request_data['likes'] = []
        request_data['parent'] = request.data.get("parent")
        # request_data['parent'] = None
        request_data['image'] = request.data.get("image")
        # tweet = Tweet('text'=request.data.get("text"),'user_id'=,)
        serializers = TweetSerializer(data=request_data)

        if serializers.is_valid():
            serializers.save()
        else:
            print("here")
            print(serializers.errors)
        return Response(serializers.data)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class UploadImage(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        pk = request.query_params.get('id', None)
        if pk:
            user = Account.objects.get(id=pk)
        else:
            user = Account.objects.get(id=request.user.id)
        serializers = UserSerializer(user)
        return Response(serializers.data)

    def put(self, request):
        user = Account.objects.get(id=request.user.id)
        serializers = UserSerializer(user, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = Account.objects.get(id=request.user.id)
        serializers = UserSerializer(user, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status.HTTP_201_CREATED)
        return Response(serializers.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = Account.objects.get(id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserFollowingSerializer

    def post(self, request):
        request_data = {}
        request_data['following_user_id'] = request.data.get("following_user_id")
        request_data['user_id'] = request.user.id
        serializers = UserFollowingSerializer(data=request_data)
        if serializers.is_valid():
            serializers.save()
        return Response(serializers.data)


class LikeAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk):
        request_data = {}
        request_data['user'] = request.user.id
        request_data['tweet_id'] = pk
        serializers = LikeSerializer(data=request_data)
        if serializers.is_valid():
            serializers.save()
        return Response(serializers.data)


class SearchTweet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'user__username']


class ImageAPI(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin, ):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    def get(self, request, pk=None):
        if (pk):
            return self.retrieve(request)
        else:
            return self.list(request)


class HashtagAPI(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin, ):
    permission_classes = [IsAuthenticated]
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()

    def get(self, request, pk=None):
        if (pk):
            return self.retrieve(request)
        else:
            return self.list(request)


class SearchByHashtag(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=key']

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
