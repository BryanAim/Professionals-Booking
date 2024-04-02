# Generated by Django 4.0.6 on 2022-09-09 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('professional', '0011_alter_prescription_patient_alter_report_professional'),
        ('sslcommerz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='api_payment_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='professional.appointment'),
        ),
    ]
