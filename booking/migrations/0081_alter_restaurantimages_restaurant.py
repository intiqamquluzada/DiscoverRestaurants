# Generated by Django 3.2 on 2023-03-12 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0080_alter_reserve_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantimages',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.restaurants'),
        ),
    ]
