from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  
from rest_framework.parsers import JSONParser
from .models import Tweet
from .serializers import TweetSerializer
def tweet_list(request):
    if request.method =='GET':
        tweets= Tweet.objects.all()
        serializers=TweetSerializer(tweets,many=True)
        return JsonResponse(serializers.data,safe=False)
    elif request.method =='Post':
        data = JSONParser().parse(request)
        serializers = TweetSerializer(data=data)

        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data,status=201)
        return JsonResponse(serializers.errors,status=400)

# Create your views here.
