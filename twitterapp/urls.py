
from django.urls import path
# from .views import tweet_list 
# from .views import TweetAPIView,TweetDetails,
from .views import GenericAPIView
urlpatterns = [
    # path('tweets/',TweetAPIView.as_view()),
    # path('tweet/<int:pk>/',TweetDetails.as_view()),
    path('generic/tweet/<int:pk>/',GenericAPIView.as_view()),
    path('generic/tweet/',GenericAPIView.as_view())
    # path('tweets/', tweet_list ),
    # path('tweet/<int:pk>/',tweetdetails)
]
