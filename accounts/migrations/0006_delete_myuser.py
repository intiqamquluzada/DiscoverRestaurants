# Generated by Django 3.2 on 2023-03-10 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_myuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]