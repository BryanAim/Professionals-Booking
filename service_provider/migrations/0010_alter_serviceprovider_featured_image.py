# Generated by Django 4.1.10 on 2024-04-07 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_provider', '0009_serviceprovider_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovider',
            name='featured_image',
            field=models.ImageField(blank=True, default='service_providers/default.png', null=True, upload_to='service_providers/'),
        ),
    ]
