from django.contrib import admin

# Register your models here.
from .models import Product, StoreManager
from .models import Cart, ServiceOrder

admin.site.register(Cart)
admin.site.register(ServiceOrder)
admin.site.register(Product)
admin.site.register(StoreManager)
