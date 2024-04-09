from django.db import models

import professional_service
from professional_service.models import User, Professional_Service_Information
# from professional.models import Professional_Information


# Create your models here.

# class Admin_Information(models.Model):
#     ADMIN_TYPE = (
#         ('hospital', 'hospital'),
#         ('laboratory', 'laboratory'),
#         ('pharmacy', 'pharmacy'),
#     )

class Admin_Information(models.Model):
    ADMIN_TYPE = (
        ('professional_service', 'Professional Service'),
        ('laboratory', 'Laboratory'),
        ('store', 'Store'),
        ('legal', 'Legal Services'),
        ('engineering', 'Engineering Services'),
        # Add other types as needed
    )

    # admin_id = models.AutoField(primary_key=True, editable=False)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='hospital_admin')
    # username = models.CharField(null=True, blank=True, max_length=200)
    # name = models.CharField(max_length=200, null=True, blank=True)
    # featured_image = models.ImageField(upload_to='admin/', default='admin/user-default.png', null=True, blank=True)
    # phone_number = models.IntegerField(null=True, blank=True)
    # email = models.CharField(max_length=200, null=True, blank=True)
    # role = models.CharField(max_length=200, choices=ADMIN_TYPE, null=True, blank=True)
    # hospital = models.ForeignKey(Hospital_Information, on_delete=models.SET_NULL, null=True, blank=True)
    
    admin_id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_service_admin')
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(null=True, blank=True, max_length=200)
    featured_image = models.ImageField(upload_to='admin/', default='admin/user-default.png', null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200, choices=ADMIN_TYPE, null=True, blank=True)
    professional_service = models.ForeignKey(Professional_Service_Information, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        # return str(self.user.username)
        return self.user.username if self.user else self.name


class Clinical_Laboratory_Technician(models.Model):
    technician_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='technician')
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='technician/', default='technician/user-default.png', null=True, blank=True)
    professional_service = models.ForeignKey(Professional_Service_Information, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return str(self.user.username)



# class hospital_department(models.Model):
#     hospital_department_id = models.AutoField(primary_key=True)
#     hospital_department_name = models.CharField(max_length=200, null=True, blank=True)
#     # professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
#     hospital = models.ForeignKey(ProfessionalService, on_delete=models.CASCADE, null=True, blank=True)
#     featured_image = models.ImageField(upload_to='departments/', default='departments/default.png', null=True, blank=True)

#     def __str__(self):
#         val1 = str(self.hospital_department_name)
#         val2 = str(self.hospital)
#         val3 = val1 + ' - ' + val2
#         return str(val3)     

class ServiceDepartment(models.Model):
    ServiceDepartment_id = models.AutoField(primary_key=True)
    ServiceDepartment_name = models.CharField(max_length=200, null=True, blank=True)
    # professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
    professional_service = models.ForeignKey(Professional_Service_Information, on_delete=models.CASCADE, null=True, blank=True)
    featured_image = models.ImageField(upload_to='profession/', default='profession/default.png', null=True, blank=True)

    def __str__(self):
        val1 = str(self.ServiceDepartment_name)
        val2 = str(self.professional_service)
        val3 = val1 + ' - ' + val2
        return str(val3)     


# class ServiceDepartment(models.Model):
#     department_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=200, unique=True)
#     description = models.TextField(blank=True, null=True)
#     featured_image = models.ImageField(upload_to='departments/', default='departments/default.png', null=True, blank=True)
    
#     def __str__(self):
#         return self.name
class specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    specialization_name = models.CharField(max_length=200, null=True, blank=True)
    # professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
    professional_service = models.ForeignKey(Professional_Service_Information, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        val1 = str(self.specialization_name)
        val2 = str(self.professional_service)
        val3 = val1 + ' - ' + val2
        return str(val3)
    
    # def __str__(self):
    #     return str(self.specialization_name)

class service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=200, null=True, blank=True)
    # professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
    professional_service = models.ForeignKey(Professional_Service_Information, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        val1 = str(self.service_name)
        val2 = str(self.professional_service)
        val3 = val1 + ' - ' + val2
        return str(val3)

class Test_Information(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    test_price = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return str(self.test_name)

    

