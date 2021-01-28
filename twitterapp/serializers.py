from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db import models
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Account, UserFollowing, Like, Image,Hashtag
from .models import Tweet


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


# class TweetSerializer(serializers.ModelSerializer):
#     likes=LikeSerializer(read_only=True, many=True)
#     class Meta:
#         model = Tweet
#         fields=['id','text','user_id','date','likes']
class TweetSerializer(serializers.ModelSerializer):
    parent = RecursiveField(allow_null=True)
    class Meta:
        model = Tweet
        fields = ['id', 'text', 'user', 'date', 'likes', 'parent','image','hashtag']


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'bio', 'birthdate', 'profile_image_url','avatar')

        extra_kwargs = {
            'password': {'write_only': True},
        }



class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ('user_id', 'following_user_id')





class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id","image"]
class UserSerializer(serializers.ModelSerializer):
    following = UserFollowingSerializer(read_only=True, many=True)
    followers = UserFollowingSerializer(read_only=True, many=True)
    tweets = TweetSerializer(read_only=True, many=True)
    liked = LikeSerializer(read_only=True, many=True)
    class Meta:
        model = Account
        fields = '__all__'
class HashtagSerializer(serializers.ModelSerializer):
    tweets= TweetSerializer(many=True)
    class Meta:
        model = Hashtag
        fields='__all__'