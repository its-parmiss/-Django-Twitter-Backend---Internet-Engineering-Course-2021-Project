# Generated by Django 3.1.5 on 2021-01-27 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0009_tweet_original_tweet_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='original_tweet_id',
        ),
        migrations.AddField(
            model_name='tweet',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='twitterapp.tweet'),
        ),
    ]
