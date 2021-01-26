
from django.urls import path
from .views import tweet_list 
urlpatterns = [
    path('tweets/', tweet_list ),
]
