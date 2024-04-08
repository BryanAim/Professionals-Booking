from django.contrib import admin

# Register your models here.
# # we are in same file path --> .models

from .models import Service_Provider_Information, Client, User

admin.site.register(User)
admin.site.register(Service_Provider_Information)
admin.site.register(Client)

