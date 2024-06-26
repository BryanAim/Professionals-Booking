# Generated by Django 4.1.10 on 2024-04-09 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('purchased', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('product_type', models.CharField(choices=[('medical', 'Medical'), ('legal', 'Legal'), ('engineering', 'Engineering Supplies'), ('art', 'Art Supplies')], max_length=200)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('stock_quantity', models.IntegerField(default=0)),
                ('featured_image', models.ImageField(blank=True, default='products/default.png', null=True, upload_to='products/')),
            ],
        ),
        migrations.CreateModel(
            name='StoreManager',
            fields=[
                ('storeManager_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('degree', models.CharField(blank=True, max_length=200, null=True)),
                ('featured_image', models.ImageField(blank=True, default='storeManager/user-default.png', null=True, upload_to='professionals/')),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='storeManager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(blank=True, max_length=200, null=True)),
                ('trans_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('orderitems', models.ManyToManyField(to='store.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL),
        ),
    ]
