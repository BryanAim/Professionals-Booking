from django.contrib import admin

# Register your models here.
# # we are in same file path --> .models

from .models import Professional_Information, Appointment, Report, ServiceRequest, Education, Experience, Specimen, Test,ServiceRequest_product,ServiceRequest_test,testCart,testOrder, Professional_review


admin.site.register(Professional_Information)
admin.site.register(Appointment)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Report)
admin.site.register(ServiceRequest)
admin.site.register(Test)
admin.site.register(Specimen)
admin.site.register(ServiceRequest_product)
admin.site.register(ServiceRequest_test)
admin.site.register(testCart)
admin.site.register(testOrder)
admin.site.register(Professional_review)
