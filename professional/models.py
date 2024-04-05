from django.db import models

import uuid

# import django user model
from service_provider.models import ServiceProvider, User, Client, Service_Provider_Information
from service_provider_admin.models import ServiceDepartment, specialization, service
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


# class Professional_Information(models.Model):
#     SERVICE_TYPE_CHOICES = (
#         ('medical', 'Medical Services'),
#         ('legal', 'Legal Services'),
#         ('engineering', 'Engineering Services'),
#         ('art', 'Art & Design'),
#         # Add more as needed
#     )
    
#     professional_id = models.AutoField(primary_key=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
#     name = models.CharField(max_length=200, null=True, blank=True)
#     username = models.CharField(max_length=200, null=True, blank=True)
#     gender = models.CharField(max_length=200, null=True, blank=True)
#     description = models.TextField(max_length=1000, null=True, blank=True)
#     department = models.CharField(max_length=200, choices=SERVICE_TYPE_CHOICES, null=True, blank=True)
#     department_name = models.ForeignKey(hospital_department, on_delete=models.SET_NULL, null=True, blank=True)
#     specialization = models.ForeignKey(specialization, on_delete=models.SET_NULL, null=True, blank=True)

#     featured_image = models.ImageField(upload_to='professionals/', default='professionals/user-default.png', null=True, blank=True)
#     certificate_image = models.ImageField(upload_to='professionals_certificate/', default='professionals_certificate/default.png', null=True, blank=True)

#     email = models.EmailField(max_length=200, null=True, blank=True)
#     phone_number = models.CharField(max_length=200, null=True, blank=True)
#     nid = models.CharField(max_length=200, null=True, blank=True)
#     availability = models.CharField(max_length=200, null=True, blank=True)
#     consultation_fee = models.IntegerField(null=True, blank=True)
#     report_fee = models.IntegerField(null=True, blank=True)
#     dob = models.CharField(max_length=200, null=True, blank=True)
    
#     # Education
#     institute = models.CharField(max_length=200, null=True, blank=True)
#     degree = models.CharField(max_length=200, null=True, blank=True)
#     completion_year = models.CharField(max_length=200, null=True, blank=True)
    
#     # work experience
#     work_place = models.CharField(max_length=200, null=True, blank=True)
#     designation = models.CharField(max_length=200, null=True, blank=True)
#     start_year = models.CharField(max_length=200, null=True, blank=True)
#     end_year = models.CharField(max_length=200, null=True, blank=True)
    
#     # register_status = models.BooleanField(default=False) default='pending'
#     register_status =  models.CharField(max_length=200, null=True, blank=True)
    
#     # ForeignKey --> one to one relationship with Hospital_Information model.
#     hospital_name = models.ForeignKey(Hospital_Information, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return str(self.user.username)


class Professional_Information(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('medical', 'Medical Services'),
        ('legal', 'Legal Services'),
        ('engineering', 'Engineering Services'),
        ('art', 'Art & Design'),
        # Add more as necessary
    )
    
    professional_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    service_type = models.CharField(max_length=200, choices=SERVICE_TYPE_CHOICES)
    department_name = models.ForeignKey(ServiceDepartment, on_delete=models.SET_NULL, null=True)
    specialization = models.ForeignKey(specialization, on_delete=models.SET_NULL, null=True)

    featured_image = models.ImageField(upload_to='professionals/', default='professionals/default.png')
    certificate_image = models.ImageField(upload_to='certificates/', default='certificates/default.png', null=True, blank=True)

    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    nid = models.CharField(max_length=200, null=True, blank=True)  # Consider if this is necessary for all professions
    availability = models.CharField(max_length=200, null=True, blank=True)
    consultation_fee = models.IntegerField(null=True, blank=True)  # Consider renaming or making this more generic
    dob = models.DateField(null=True, blank=True)
    
    # ForeignKey --> one to one relationship with Hospital_Information model.
    service_provider_name = models.ForeignKey(Service_Provider_Information, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    department = models.CharField(max_length=200, choices=SERVICE_TYPE_CHOICES, null=True, blank=True)
    report_fee = models.IntegerField(null=True, blank=True)

        # Education
    institute = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    completion_year = models.CharField(max_length=200, null=True, blank=True)
    
    # work experience
    work_place = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    start_year = models.CharField(max_length=200, null=True, blank=True)
    end_year = models.CharField(max_length=200, null=True, blank=True)

    register_status = models.CharField(max_length=200, null=True, blank=True)  # Consider using a boolean if just tracking registration status
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.SET_NULL, null=True)  # Generalized from hospital

    def __str__(self):
        return self.user.username if self.user else self.name



# class Appointment(models.Model):
#     # ('database value', 'display_name')
#     APPOINTMENT_TYPE = (
#         ('report', 'report'),
#         ('checkup', 'checkup'),
#     )
#     APPOINTMENT_STATUS = (
#         ('pending', 'pending'),
#         ('confirmed', 'confirmed'),
#         ('cancelled', 'cancelled'),
#     )

#     id = models.AutoField(primary_key=True)
#     date = models.DateField(null=True, blank=True)
#     time = models.CharField(max_length=200, null=True, blank=True)
#     professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE, null=True, blank=True)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
#     appointment_type = models.CharField(max_length=200, choices=APPOINTMENT_TYPE)
#     appointment_status = models.CharField(max_length=200, choices=APPOINTMENT_STATUS)
#     serial_number = models.CharField(max_length=200, null=True, blank=True)
#     payment_status = models.CharField(max_length=200, null=True, blank=True, default='pending')
#     transaction_id = models.CharField(max_length=255, null=True, blank=True)
#     message = models.CharField(max_length=255, null=True, blank=True)
    

#     def __str__(self):
#         return str(self.client.username)

class Appointment(models.Model):
    APPOINTMENT_TYPE_CHOICES = (
        ('consultation', 'Consultation'),
        ('service', 'Service'),
        # Extend as necessary
    )
    APPOINTMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    appointment_id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.CharField(max_length=200)
    professional = models.ForeignKey(Professional_Information, on_delete=models.CASCADE)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    appointment_type = models.CharField(max_length=200, choices=APPOINTMENT_TYPE_CHOICES)
    appointment_status = models.CharField(max_length=200, choices=APPOINTMENT_STATUS_CHOICES)
    notes = models.TextField(null=True, blank=True)  # To replace 'message', more general

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

        
class Prescription(models.Model):
    # product name, quantity, days, time, description, test, test_descrip
    prescription_id = models.AutoField(primary_key=True)
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

class Prescription_product(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    frequency = models.CharField(max_length=200, null=True, blank=True)
    relation_with_meal = models.CharField(max_length=200, null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.prescription.prescription_id)

class Prescription_test(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True, blank=True)
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    test_description = models.TextField(null=True, blank=True)
    test_info_id = models.CharField(max_length=200, null=True, blank=True)
    test_info_price = models.CharField(max_length=200, null=True, blank=True)
    test_info_pay_status = models.CharField(max_length=200, null=True, blank=True)
    
    """
    (create prescription)
    professional input --> test_id 
    using test_id --> retrive price
    store price in prescription_test column
    """

    def __str__(self):
        return str(self.prescription.prescription_id)
    
# # test cart system
class testCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_cart')
    item = models.ForeignKey(Prescription_test, on_delete=models.CASCADE)
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