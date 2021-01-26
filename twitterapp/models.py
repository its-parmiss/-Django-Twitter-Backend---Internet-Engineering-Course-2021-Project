from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.
class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=280)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    date= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name