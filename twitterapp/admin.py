from django.contrib import admin
from .models import Tweet, Account, UserFollowing

admin.site.register(Tweet)
admin.site.register(Account)
admin.site.register(UserFollowing)
# Register your models here.
