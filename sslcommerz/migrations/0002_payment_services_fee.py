# Generated by Django 4.1.10 on 2024-04-09 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sslcommerz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='services_fee',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
