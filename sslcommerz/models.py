from django.db import models
from professional.models import Appointment, testOrder, Prescription
from service_provider.models import Client
from store.models import ServiceOrder

# Create your models here.


class Payment(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    # order = models.ForeignKey(ServiceOrder, on_delete=models.SET_NULL, null=True, blank=True)
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.SET_NULL, null=True, blank=True)
    # test_order = models.ForeignKey(testOrder, on_delete=models.SET_NULL, null=True, blank=True)
    # prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True)
    
    payment_type = models.CharField(max_length=200, null=True, blank=True)
    
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    val_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    currency_amount = models.CharField(max_length=255, null=True, blank=True)
    consulation_fee = models.CharField(max_length=255, null=True, blank=True)
    services_fee = models.CharField(max_length=255, null=True, blank=True)
    
    card_type = models.CharField(max_length=255, null=True, blank=True)
    card_no = models.CharField(max_length=255, null=True, blank=True)
    bank_transaction_id = models.CharField(
        max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    transaction_date = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255, null=True, blank=True)
    card_issuer = models.CharField(max_length=255, null=True, blank=True)
    card_brand = models.CharField(max_length=255, null=True, blank=True)
    
    # Pharamcy
    # {% url 'ssl-payment-request-product' pk=order.user.patient.patient_id id=order.id %}
    # order.orderitems.all.1
    
    

    # String representation of object
    def __str__(self):
        return str(self.name)
