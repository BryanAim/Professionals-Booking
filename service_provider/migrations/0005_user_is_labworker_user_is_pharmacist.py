# Generated by Django 4.1.10 on 2024-04-06 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_provider', '0004_rename_is_admin_user_is_service_provider_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_labworker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_pharmacist',
            field=models.BooleanField(default=False),
        ),
    ]