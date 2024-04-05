from django.contrib import admin

# Register your models here.
# # we are in same file path --> .models

from .models import ServiceProvider, Client, User

admin.site.register(User)
admin.site.register(ServiceProvider)
admin.site.register(Client)

