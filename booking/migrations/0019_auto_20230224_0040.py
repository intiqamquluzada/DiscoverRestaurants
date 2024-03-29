# Generated by Django 3.2 on 2023-02-23 20:40

from django.db import migrations, models
import django.db.models.deletion
import services.uploader


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0018_alter_blogmodel_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurants',
            name='menu',
        ),
        migrations.CreateModel(
            name='RestaurantMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('images', models.FileField(upload_to=services.uploader.Uploader.upload_images_to_restaurants)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.restaurants')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
