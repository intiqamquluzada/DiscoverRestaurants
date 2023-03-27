# Generated by Django 3.2 on 2023-03-26 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0097_remove_blogmodel_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
            options={
                'verbose_name': 'Əlaqə yaratmaq istəyən şəxs',
                'verbose_name_plural': 'Əlaqə yaratmaq istəyən şəxslər',
                'ordering': ('-created_at',),
            },
        ),
    ]