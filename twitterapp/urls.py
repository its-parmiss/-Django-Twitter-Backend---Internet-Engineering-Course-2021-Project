
from django.urls import path
# from .views import tweet_list 
# from .views import TweetAPIView,TweetDetails,
from .views import GenericAPIView,RegisterApi,UserAPIView,FollowAPIView,uploadProfileImageAPI,LikeAPIView
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path('tweets/',TweetAPIView.as_view()),
    # path('tweet/<int:pk>/',TweetDetails.as_view()),
    path('generic/tweet/<int:pk>/',GenericAPIView.as_view()),
    path('generic/tweet/',GenericAPIView.as_view()),
    path('generic/register/', RegisterApi.as_view()),
    path('generic/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('generic/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('generic/follow/',FollowAPIView.as_view()),
    path('generic/user/',UserAPIView.as_view()),
    path('generic/upload_profile/',uploadProfileImageAPI.as_view()),
    path('generic/like/<int:pk>/',LikeAPIView.as_view())
    # path('tweets/', tweet_list ),
    # path('tweet/<int:pk>/',tweetdetails)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
