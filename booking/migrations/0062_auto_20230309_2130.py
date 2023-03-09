# Generated by Django 3.2 on 2023-03-09 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0061_reserve_reserved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurantforreserve', to='booking.restaurants'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
