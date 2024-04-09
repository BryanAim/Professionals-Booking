from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# from django.contrib.auth.models import User

from .models import Professional_Information
from professional_service.models import User


# # from django.core.mail import send_mail
# # from django.conf import settings


@receiver(post_save, sender=Professional_Information)
def updateUser(sender, instance, created, **kwargs):
    # user.profile or below (1-1 relationship goes both ways)
    professional = instance
    user = professional.user

    if created == False:
        user.first_name = professional.name
        user.username = professional.username
        user.email = professional.email
        user.address = professional.address
        user.save()
