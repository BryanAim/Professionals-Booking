# Generated by Django 4.1.10 on 2024-04-09 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service_provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_Information',
            fields=[
                ('test_id', models.AutoField(primary_key=True, serialize=False)),
                ('test_name', models.CharField(blank=True, max_length=200, null=True)),
                ('test_price', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='specialization',
            fields=[
                ('specialization_id', models.AutoField(primary_key=True, serialize=False)),
                ('specialization_name', models.CharField(blank=True, max_length=200, null=True)),
                ('service_provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service_provider.service_provider_information')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceDepartment',
            fields=[
                ('ServiceDepartment_id', models.AutoField(primary_key=True, serialize=False)),
                ('ServiceDepartment_name', models.CharField(blank=True, max_length=200, null=True)),
                ('featured_image', models.ImageField(blank=True, default='profession/default.png', null=True, upload_to='profession/')),
                ('service_provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service_provider.service_provider_information')),
            ],
        ),
        migrations.CreateModel(
            name='service',
            fields=[
                ('service_id', models.AutoField(primary_key=True, serialize=False)),
                ('service_name', models.CharField(blank=True, max_length=200, null=True)),
                ('service_provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service_provider.service_provider_information')),
            ],
        ),
        migrations.CreateModel(
            name='Clinical_Laboratory_Technician',
            fields=[
                ('technician_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('featured_image', models.ImageField(blank=True, default='technician/user-default.png', null=True, upload_to='technician/')),
                ('service_provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_provider.service_provider_information')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='technician', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Admin_Information',
            fields=[
                ('admin_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('featured_image', models.ImageField(blank=True, default='admin/user-default.png', null=True, upload_to='admin/')),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('role', models.CharField(blank=True, choices=[('service_provider', 'Service Provider'), ('laboratory', 'Laboratory'), ('store', 'Store'), ('legal', 'Legal Services'), ('engineering', 'Engineering Services')], max_length=200, null=True)),
                ('service_provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_provider.service_provider_information')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_provider_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]