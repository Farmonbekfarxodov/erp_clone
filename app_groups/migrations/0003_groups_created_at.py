# Generated by Django 5.1.6 on 2025-03-17 12:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_groups', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
