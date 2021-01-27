
from django.urls import path
from .views import tweet_list 
from .views import tweetdetails
urlpatterns = [
    path('tweets/', tweet_list ),
    path('tweet/<int:pk>/',tweetdetails)
]
