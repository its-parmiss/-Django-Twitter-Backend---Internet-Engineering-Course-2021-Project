from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Account(User):
    profile_image = models.ImageField(blank=True)
    bio = models.CharField(max_length=280, default="")
    birthdate = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.username


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=280, default="")
    date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey("Account", related_name="tweets", on_delete=models.CASCADE)
    original_tweet_id = models.IntegerField(null=True,blank=True)



class UserFollowing(models.Model):
    user_id = models.ForeignKey("Account", related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey("Account", related_name="followers", on_delete=models.CASCADE)
    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    tweet_id = models.ForeignKey(Tweet, related_name="likes", on_delete=models.CASCADE)
    user_id = models.ForeignKey(Account, related_name="liked", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
