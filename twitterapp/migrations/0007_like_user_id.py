# Generated by Django 3.1.5 on 2021-01-27 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0006_auto_20210128_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='user_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='twitterapp.account'),
            preserve_default=False,
        ),
    ]
