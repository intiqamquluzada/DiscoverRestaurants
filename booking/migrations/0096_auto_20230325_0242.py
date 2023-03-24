# Generated by Django 3.2 on 2023-03-24 22:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0095_auto_20230325_0241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='blogmodel',
            name='user',
            field=models.ForeignKey(default='32', on_delete=django.db.models.deletion.CASCADE, related_name='userblog', to='accounts.myuser'),
            preserve_default=False,
        ),
    ]
