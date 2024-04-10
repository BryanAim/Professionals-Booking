from django.db import models
from django.conf import settings
import uuid
from professional.models import ServiceRequest

from professional_service.models import User, Client


# Create your models here.

class StoreManager(models.Model):
    storeManager_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='storeManager')
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ImageField(upload_to='professionals/', default='storeManager/user-default.png', null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


    
class Product(models.Model):
    PRODUCT_TYPE_CHOICES = (
        # Extend this to include non-medication items
        ('medical', 'Medical'),
        ('legal', 'Legal'),
        ('engineering', 'Engineering Supplies'),
        ('art', 'Art Supplies'),
        # etc.
    )
    product_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    product_type = models.CharField(max_length=200, choices=PRODUCT_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    featured_image = models.ImageField(upload_to='products/', default='products/default.png', null=True, blank=True)
    # Extend or modify attributes as needed

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.quantity} X {self.item}'
    
    # Each product total
    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total
    

class ServiceOrder(models.Model):
    # id
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=200, blank=True, null=True)
    trans_ID = models.CharField(max_length=200, blank=True, null=True)

    # Subtotal
    def get_totals(self):
        total = 0 
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total
    
    # Count Cart Items
    def count_cart_items(self):
        return self.orderitems.count()
    
    # Stock Calculation
    def stock_quantity_decrease(self):
        for order_item in self.orderitems.all():
            decrease_stock= order_item.item.stock_quantity - order_item.quantity
            order_item.item.stock_quantity = decrease_stock 
            order_item.item.stock_quantity.save()
            return decrease_stock
    
    # TOTAL
    def final_bill(self):
        delivery_price= 40.00
        Bill = self.get_totals()+ delivery_price
        float_Bill = format(Bill, '0.2f')
        return float_Bill
    
