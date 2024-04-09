from django.contrib import admin

# Register your models here.
# # we are in same file path --> .models

from .models import Professional_Service_Information, Client, User

admin.site.register(User)
admin.site.register(Professional_Service_Information)
admin.site.register(Client)

