from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from service_provider.models import User
from .models import Professional_Information
# # Create a custom form that inherits from user form (reason --> for modify and customize)


class ProfessionalUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # password1 and password2 are required fields (django default)
        fields = ['username', 'email', 'password1', 'password2', 'address']
        # labels = {
        #     'first_name': 'Name',
        # }

    # create a style for model form
    def __init__(self, *args, **kwargs):
        super(ProfessionalUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control floating'})


class ProfessionalForm(ModelForm):
    class Meta:
        model = Professional_Information
        fields = ['name', 'email', 'phone_number', 'degree', 'profession',
                  'featured_image', 'availability', 'consultation_fee', 'address','service_name']

    def __init__(self, *args, **kwargs):
        super(ProfessionalForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
