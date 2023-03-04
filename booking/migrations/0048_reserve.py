# Generated by Django 3.2 on 2023-03-04 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0047_alter_rating_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('count_of_adult', models.IntegerField(default=1)),
                ('count_of_children', models.IntegerField(default=1)),
                ('phone_number', models.TextField()),
                ('passport_number', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Reserve',
                'verbose_name_plural': 'Reserves',
                'ordering': ('-created_at',),
            },
        ),
    ]
