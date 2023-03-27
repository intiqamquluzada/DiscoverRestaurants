# Generated by Django 3.2 on 2023-03-24 22:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0094_alter_restaurants_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='blogmodel',
            name='user',
            field=models.ManyToManyField(related_name='userblog', to=settings.AUTH_USER_MODEL),
        ),
    ]