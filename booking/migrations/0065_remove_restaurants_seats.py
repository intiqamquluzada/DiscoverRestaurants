# Generated by Django 3.2 on 2023-03-09 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0064_auto_20230309_2156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurants',
            name='seats',
        ),
    ]
