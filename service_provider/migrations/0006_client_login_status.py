# Generated by Django 4.1.10 on 2024-04-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_provider', '0005_user_is_labworker_user_is_pharmacist'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='login_status',
            field=models.CharField(blank=True, default='offline', max_length=200, null=True),
        ),
    ]
