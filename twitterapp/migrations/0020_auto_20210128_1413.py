# Generated by Django 3.1.5 on 2021-01-28 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0019_auto_20210128_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='hashtag',
        ),
        migrations.AddField(
            model_name='tweet',
            name='hashtag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tweets', to='twitterapp.hashtag'),
        ),
    ]