from django.contrib import admin

# Register your models here.
from .models import Admin_Information, Technical_Specialist, ServiceDepartment, specialization, service ,Test_Information

admin.site.register(Admin_Information)

admin.site.register(Technical_Specialist)

admin.site.register(ServiceDepartment)

admin.site.register(specialization)

admin.site.register(service)

admin.site.register(Test_Information)
