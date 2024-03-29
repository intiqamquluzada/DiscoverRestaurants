# Generated by Django 3.2 on 2023-02-25 10:35

from django.db import migrations, models
import services.uploader


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0023_rename_qr_code_restaurantmenu_qr_code_x'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurants',
            name='qrcode_image',
            field=models.ImageField(blank=True, upload_to=services.uploader.Uploader.upload_images_for_menu),
        ),
        migrations.DeleteModel(
            name='RestaurantMenu',
        ),
    ]
