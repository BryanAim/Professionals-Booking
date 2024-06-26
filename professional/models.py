from django.db import models

import uuid

# import django user model
from professional_service.models import  User, Client, Professional_Service_Information
from professional_service_admin.models import ServiceDepartment, specialization, service
from django.conf import settings


# # Create your models here.

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
# Create your models here.


class Professional_Information(models.Model):
    PROFESSION_CHOICES = (
        ('medical', 'Medical Services'),
        ('legal', 'Legal Services'),
        ('engineering', 'Engineering Services'),
        ('art', 'Art & Design'),
        # Add more as necessary
    )
    
    professional_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    profession = models.CharField(max_length=200, choices=PROFESSION_CHOICES)
    profession_name = models.ForeignKey(ServiceDepartment, on_delete=models.SET_NULL, null=True)
    specialization = models.ForeignKey(specialization, on_delete=models.SET_NULL, null=True)

    featured_image = models.ImageField(upload_to='professionals/', default='professionals/user-default.png')
    certificate_image = models.ImageField(upload_to='professionals_certificates/', default='professionals_certificates/default.png', null=True, blank=True)

    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    availability = models.CharField(max_length=200, null=True, blank=True, default='9am - 4pm')
    consultation_fee = models.IntegerField(null=True, blank=True, default=0)
    services_fee = models.IntegerField(null=True, blank=True, default=0)
    address = models.CharField(max_length=200, null=True, blank=True)
    
    # ForeignKey --> one to one relationship with Hospital_Information model.
    service_name = models.ForeignKey(Professional_Service_Information, on_delete=models.SET_NULL, null=True, blank=True)

    profession = models.CharField(max_length=200, choices=PROFESSION_CHOICES, null=True, blank=True)
    

        # Education
    institute = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    completion_year = models.CharField(max_length=200, null=True, blank=True)
    
    # work experience
    work_place = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    start_year = models.CharField(max_length=200, null=True, blank=True)
    end_year = models.CharField(max_length=200, null=True, blank=True)

    register_status = models.CharField(max_length=200, null=True, blank=True, default='Accepted')  

    def __str__(self):
        return self.user.username if self.user else self.name



class Appointment(models.Model):
    APPOINTMENT_TYPE = (
        ('consultation_app', 'Consultation'),
        ('service_app', 'Service'),
        # Extend as necessary
    )
    APPOINTMENT_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=200, null=True, blank=True)
    professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    appointment_type = models.CharField(max_length=200, choices=APPOINTMENT_TYPE)
    appointment_status = models.CharField(max_length=200, choices=APPOINTMENT_STATUS)
    serial_number = models.CharField(max_length=200, null=True, blank=True)
    payment_status = models.CharField(max_length=200, null=True, blank=True, default='pending')
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.client.username} - {self.date} - {self.time}"


class Education(models.Model):
    education_id = models.AutoField(primary_key=True)
    professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    institute = models.CharField(max_length=200, null=True, blank=True)
    year_of_completion = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.professional.name)
    
class Experience(models.Model):
    experience_id = models.AutoField(primary_key=True)
    professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
    work_place_name = models.CharField(max_length=200, null=True, blank=True)
    from_year = models.CharField(max_length=200, null=True, blank=True)
    to_year = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.professional.name)


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    professional = models.ForeignKey(Professional_Information, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    specimen_id = models.CharField(max_length=200, null=True, blank=True)
    specimen_type = models.CharField(max_length=200, null=True, blank=True)
    collection_date = models.CharField(max_length=200, null=True, blank=True)
    receiving_date = models.CharField(max_length=200, null=True, blank=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    result = models.CharField(max_length=200, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    referred_value = models.CharField(max_length=200, null=True, blank=True)
    delivery_date = models.CharField(max_length=200, null=True, blank=True)
    other_information = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.client.username)

class Specimen(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    specimen_id = models.AutoField(primary_key=True)
    specimen_type = models.CharField(max_length=200, null=True, blank=True)
    collection_date = models.CharField(max_length=200, null=True, blank=True)
    receiving_date = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.report.report_id)

class Test(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    result = models.CharField(max_length=200, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    referred_value = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.report.report_id)

        
class ServiceRequest(models.Model):
    # product name, quantity, days, time, description, test, test_descrip
    serviceRequest_id = models.AutoField(primary_key=True)
    professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    create_date = models.CharField(max_length=200, null=True, blank=True)
    product_name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.CharField(max_length=200, null=True, blank=True)
    days = models.CharField(max_length=200, null=True, blank=True)
    time = models.CharField(max_length=200, null=True, blank=True)
    relation_with_meal = models.CharField(max_length=200, null=True, blank=True)
    product_description = models.TextField(null=True, blank=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    test_description = models.TextField(null=True, blank=True)
    extra_information = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.client.username)

class ServiceRequest_product(models.Model):
    serviceRequest = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    frequency = models.CharField(max_length=200, null=True, blank=True)
    relation_with_meal = models.CharField(max_length=200, null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.serviceRequest.serviceRequest_id)

class ServiceRequest_test(models.Model):
    serviceRequest = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True, blank=True)
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    test_description = models.TextField(null=True, blank=True)
    test_info_id = models.CharField(max_length=200, null=True, blank=True)
    test_info_price = models.CharField(max_length=200, null=True, blank=True)
    test_info_pay_status = models.CharField(max_length=200, null=True, blank=True)
    
    """
    (create serviceRequest)
    professional input --> test_id 
    using test_id --> retrive price
    store price in serviceRequest_test column
    """

    def __str__(self):
        return str(self.serviceRequest.serviceRequest_id)
    
# # test cart system
class testCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_cart')
    item = models.ForeignKey(ServiceRequest_test, on_delete=models.CASCADE)
    name = models.CharField(default='test', max_length=200)
    # quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.item.test_info_id} X {self.item.test_name}'

    def get_total(self): 
        total = self.item.test_info_price
        
        return total

class testOrder(models.Model):
    # id
    orderitems = models.ManyToManyField(testCart)
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
    
    # TOTAL
    def final_bill(self):
        vat= 20.00
        Bill = self.get_totals()+ vat
        float_Bill = format(Bill, '0.2f')
        return float_Bill

class Professional_review(models.Model):
    review_id = models.AutoField(primary_key=True)
    professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.client.username)