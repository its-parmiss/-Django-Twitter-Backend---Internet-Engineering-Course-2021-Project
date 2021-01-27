# Generated by Django 3.1.5 on 2021-01-27 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0008_auto_20210128_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='original_tweet',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='twitterapp.tweet'),
        ),
    ]