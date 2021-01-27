from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=280)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    date= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Account(User):  
    followingCount=models.IntegerField(default=0)
    followerCount=models.IntegerField(default=0)
    profile_image = models.ImageField(blank=True)
    def __unicode__(self):
        return self.username


class UserFollowing(models.Model):
    user_id = models.ForeignKey("Account", related_name="following",on_delete=models.CASCADE)
    following_user_id = models.ForeignKey("Account", related_name="followers",on_delete=models.CASCADE)
    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)
