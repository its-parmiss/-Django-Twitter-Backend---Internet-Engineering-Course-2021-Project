from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
# from .views import tweet_list
# from .views import TweetAPIView,TweetDetails,
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt import views as jwt_views

from .views import GenericAPIView, RegisterApi, UserAPIView, FollowAPIView, LikeAPIView, UploadImage,ImageAPI,HashtagAPI
from .views import GenericAPIView, RegisterApi, UserAPIView, FollowAPIView, LikeAPIView, UploadImage
from .views import SearchTweet

urlpatterns = [
    # path('tweets/',TweetAPIView.as_view()),
    # path('tweet/<int:pk>/',TweetDetails.as_view()),
    path('generic/tweet/<int:pk>/', csrf_exempt(GenericAPIView.as_view())),
    path('generic/tweet/', csrf_exempt(GenericAPIView.as_view())),
    path('generic/register/', csrf_exempt(RegisterApi.as_view())),
    path('generic/token/', csrf_exempt(jwt_views.TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('generic/token/refresh/', csrf_exempt(jwt_views.TokenRefreshView.as_view()), name='token_refresh'),
    path('generic/follow/', csrf_exempt(FollowAPIView.as_view())),
    path('generic/user/', csrf_exempt(UserAPIView.as_view())),
    path('generic/upload_profile/', csrf_exempt(UploadImage.as_view())),
    path('generic/image/', csrf_exempt(ImageAPI.as_view())),
    path('generic/image/<int:pk>/', csrf_exempt(ImageAPI.as_view())),
    path('generic/like/<int:pk>/', csrf_exempt(LikeAPIView.as_view())),
    path('generic/explore/', csrf_exempt(SearchTweet.as_view({'get': 'list'}))),
    path('generic/hashtag/<int:pk>/', csrf_exempt(HashtagAPI.as_view())),
    path('generic/hashtag/', csrf_exempt(HashtagAPI.as_view())),

    # path('tweets/', tweet_list ),
    # path('tweet/<int:pk>/',tweetdetails)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
