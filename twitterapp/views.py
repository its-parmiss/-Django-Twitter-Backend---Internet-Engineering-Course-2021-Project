from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  
from rest_framework.parsers import JSONParser
from .models import Tweet
from .serializers import TweetSerializer
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def tweet_list(request):
    if request.method =='GET':
        tweets= Tweet.objects.all()
        serializers=TweetSerializer(tweets,many=True)
        return JsonResponse(serializers.data,safe=False)
    elif request.method =='POST':
        data = JSONParser().parse(request)
        serializers = TweetSerializer(data=data)

        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data,status=201)
        return JsonResponse(serializers.errors,status=400)
@csrf_exempt
def tweetdetails(request,pk):
    try:
        tweet=Tweet.objects.get(pk=pk)

    except Tweet.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='GET':
        serializers=TweetSerializer(tweet)
        return JsonResponse(serializers.data)
    elif request.method =='PUT':
        data = JSONParser().parse(request)
        serializers = TweetSerializer(tweet,data=data)

        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data)
        return JsonResponse(serializers.errors,status=400)
    elif request.method =='DELETE':
        tweet.delete()
        return HttpResponse(status=204)
# Create your views here.
