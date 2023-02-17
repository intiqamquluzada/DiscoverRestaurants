# Generated by Django 3.2 on 2023-02-15 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_auto_20230216_0215'),
    ]

    operations = [
        migrations.AddField(
            model_name='cities',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.countries'),
        ),
        migrations.AlterField(
            model_name='cities',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
