from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# from django.contrib.auth.models import User
from .models import Client, User
from professional.models import Professional_Information
from service_provider_admin.models import Admin_Information, Clinical_Laboratory_Technician

from store.models import StoreManager

import random
import string


# # from django.core.mail import send_mail
# # from django.conf import settings


# error here --> two signals are working at the same time


# @receiver(post_save, sender=User)
# def createPatient(sender, instance, created, **kwargs):
#     if created:
#         Patient.objects.create(user=instance)

def generate_random_string():
    N = 6
    string_var = ""
    string_var = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=N))
    string_var = "#PT" + string_var
    return string_var

@receiver(post_save, sender=User)
def createClient(sender, instance, created, **kwargs):
    if created:
        if instance.is_client:
            user = instance
            Client.objects.create(
                user=user, username=user.username, email=user.email, serial_number = generate_random_string())
        elif instance.is_professional:
            user = instance
            Professional_Information.objects.create(
                user=user, username=user.username, email=user.email, address=user.address)
        elif instance.is_service_provider_admin:
            user = instance
            Admin_Information.objects.create(
                user=user, username=user.username, email=user.email)
        elif instance.is_storeManager:
            user = instance
            StoreManager.objects.create(user=user, username=user.username, email=user.email)
        elif instance.is_labworker:
            user = instance
            Clinical_Laboratory_Technician.objects.create(user=user, username=user.username, email=user.email)
        


@receiver(post_save, sender=Client)
def updateUser(sender, instance, created, **kwargs):
    # user.profile or below (1-1 relationship goes both ways)
    client = instance
    user = client.user

    if created == False:
        user.first_name = client.name
        user.username = client.username
        user.age = client.age
        user.phone_number = client.phone_number
        user.history = client.history
        user.email = client.email
        user.address = client.address
        user.save()


# @receiver(post_save, sender=User)
# def createProfessional(sender, instance, created, **kwargs):
#     if created:
#         Professional_Information.objects.create(user=instance)
