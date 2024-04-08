# Generated by Django 4.1.10 on 2024-04-08 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('professional', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service_provider_admin', '0001_initial'),
        ('service_provider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='testcart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='professional.prescription_test'),
        ),
        migrations.AddField(
            model_name='testcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_cart', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='test',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='professional.report'),
        ),
        migrations.AddField(
            model_name='specimen',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='professional.report'),
        ),
        migrations.AddField(
            model_name='report',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service_provider.client'),
        ),
        migrations.AddField(
            model_name='report',
            name='professional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='professional.professional_information'),
        ),
        migrations.AddField(
            model_name='professional_review',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service_provider.client'),
        ),
        migrations.AddField(
            model_name='professional_review',
            name='professional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='professional.professional_information'),
        ),
        migrations.AddField(
            model_name='professional_information',
            name='service_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_provider.service_provider_information'),
        ),
        migrations.AddField(
            model_name='professional_information',
            name='service_type_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_provider_admin.servicedepartment'),
        ),
        migrations.AddField(
            model_name='professional_information',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_provider_admin.specialization'),
        ),
        migrations.AddField(
            model_name='professional_information',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prescription_test',
            name='prescription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='professional.prescription'),
        ),
        migrations.AddField(
            model_name='prescription_product',
            name='prescription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='professional.prescription'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_provider.client'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='professional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='professional.professional_information'),
        ),
        migrations.AddField(
            model_name='experience',
            name='professional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='professional.professional_information'),
        ),
        migrations.AddField(
            model_name='education',
            name='professional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='professional.professional_information'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service_provider.client'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='professional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='professional.professional_information'),
        ),
    ]
