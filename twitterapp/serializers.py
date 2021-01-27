from rest_framework import serializers
from .models import Tweet

from django.db import models
from .models import Account,UserFollowing
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields=['id','text','username','name','date']

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','username','password','first_name', 'last_name','email','bio','birthdate','profile_image')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = Account.objects.create_user(validated_data['username'],     password = validated_data['password']  ,first_name=validated_data['first_name'],  last_name=validated_data['last_name'], email=validated_data['email'],followingCount=0,followerCount=0)
        return user

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ('user_id','following_user_id')
class UserSerializer(serializers.ModelSerializer):
    following = UserFollowingSerializer(read_only=True, many=True)
    followers=UserFollowingSerializer(read_only=True, many=True)
    class Meta:
        model = Account
        fields = '__all__'
