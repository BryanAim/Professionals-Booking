from django.db import models
import uuid
from django.conf import settings


# import django user model
from django.contrib.auth.models import AbstractUser


# Create your models here.

"""
null=True --> don't require a value when inserting into the database
blank=True --> allow blank value when submitting a form
auto_now_add --> automatically set the value to the current date and time
unique=True --> prevent duplicate values
primary_key=True --> set this field as the primary key
editable=False --> prevent the user from editing this field

django field types --> google it  # every field types has field options
Django automatically creates id field for each model class which will be a PK # primary_key=True --> if u want to set manual
"""

class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_professional = models.BooleanField(default=False)
    is_professional_service_admin = models.BooleanField(default=False)
    is_technicalSpecialist = models.BooleanField(default=False)
    is_storeManager = models.BooleanField(default=False)
    #login_status = models.CharField(max_length=200, null=True, blank=True, default="offline")
    login_status = models.BooleanField(default=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    
# class Hospital_Information(models.Model):
#     # ('database value', 'display_name')
#     HOSPITAL_TYPE = (
#         ('private', 'Private hospital'),
#         ('public', 'Public hospital'),
#     )

#     hospital_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=200, null=True, blank=True)
#     address = models.CharField(max_length=200, null=True, blank=True)
#     featured_image = models.ImageField(upload_to='hospitals/', default='hospitals/default.png', null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     email = models.EmailField(max_length=200, null=True, blank=True)
#     phone_number = models.IntegerField(null=True, blank=True)
#     hospital_type = models.CharField(max_length=200, choices=HOSPITAL_TYPE)
#     general_bed_no = models.IntegerField(null=True, blank=True)
#     available_icu_no = models.IntegerField(null=True, blank=True)
#     regular_cabin_no = models.IntegerField(null=True, blank=True)
#     emergency_cabin_no = models.IntegerField(null=True, blank=True)
#     vip_cabin_no = models.IntegerField(null=True, blank=True)
    

#     # String representation of object
#     def __str__(self):
#         return str(self.name)



class Professional_Service_Information(models.Model):
    # ('database value', 'display_name')
    PROFESSION = (
        ('medical', 'Medical Services'),
        ('legal', 'Legal Services'),
        ('engineering', 'Engineering Services'),
        ('art', 'Art & Design'),
        ('tech', 'Technology Services'),
        ('education', 'Educational Services'),
        ('consulting', 'Consulting Services'),
    )

    professional_service_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    # address = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ImageField(upload_to='professional_services/', default='professional_services/default.png', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # email = models.EmailField(max_length=200, null=True, blank=True)
    # phone_number = models.IntegerField(null=True, blank=True)
    profession = models.CharField(max_length=200, choices=PROFESSION)
    # general_bed_no = models.IntegerField(null=True, blank=True)
    # available_icu_no = models.IntegerField(null=True, blank=True)
    # regular_cabin_no = models.IntegerField(null=True, blank=True)
    # emergency_cabin_no = models.IntegerField(null=True, blank=True)
    # vip_cabin_no = models.IntegerField(null=True, blank=True)
    

    # String representation of object
    def __str__(self):
        return str(self.name)


# class Patient(models.Model):
#     patient_id = models.AutoField(primary_key=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='patient')
#     name = models.CharField(max_length=200, null=True, blank=True)
#     username = models.CharField(max_length=200, null=True, blank=True)
#     age = models.IntegerField(null=True, blank=True)
#     email = models.EmailField(max_length=200, null=True, blank=True)
#     phone_number = models.IntegerField(null=True, blank=True)
#     address = models.CharField(max_length=200, null=True, blank=True)
#     featured_image = models.ImageField(upload_to='patients/', default='patients/user-default.png', null=True, blank=True)
#     blood_group = models.CharField(max_length=200, null=True, blank=True)
#     history = models.CharField(max_length=200, null=True, blank=True)
#     dob = models.CharField(max_length=200, null=True, blank=True)
#     nid = models.CharField(max_length=200, null=True, blank=True)
#     serial_number = models.CharField(max_length=200, null=True, blank=True)
    
#     # Chat
#     login_status = models.CharField(max_length=200, null=True, blank=True, default="offline")

#     def __str__(self):
#         return str(self.user.username)

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='client')
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True, default=0)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True, default=254712345678)
    address = models.CharField(max_length=200, null=True, blank=True)
    # Keep common fields and consider adding or modifying fields to suit a general use case
    featured_image = models.ImageField(upload_to='clients/', default='clients/user-default.png', null=True, blank=True)
    # Remove or generalize medical-specific fields
    # Add additional fields if necessary to accommodate information relevant to clients of various services
    history = models.CharField(max_length=200, null=True, blank=True)
    # dob = models.CharField(max_length=200, null=True, blank=True)
    
    blood_group = models.CharField(max_length=200, null=True, blank=True)
    # nid = models.CharField(max_length=200, null=True, blank=True)

    
    serial_number = models.CharField(max_length=200, null=True, blank=True)
    
    # Chat
    login_status = models.CharField(max_length=200, null=True, blank=True, default="offline")

    def __str__(self):
        return self.user.username



