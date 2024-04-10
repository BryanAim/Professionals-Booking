from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from professional_service.models import User, Professional_Service_Information
from .models import Admin_Information, Technical_Specialist

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # create a style for model form
    def __init__(self, *args, **kwargs):
        super(AdminUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            

class TechnicalSpecialistCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # create a style for model form
    def __init__(self, *args, **kwargs):
        super(TechnicalSpecialistCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class StoreManagerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # create a style for model form
    def __init__(self, *args, **kwargs):
        super(StoreManagerCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

# class EditTechnicalSpecialistForm(forms.ModelForm):
#     class Meta:
#         model = Technical_Specialist
#         fields = ['name', 'age', 'phone_number', 'featured_image']

#     def __init__(self, *args, **kwargs):
#         super(EditTechnicalSpecialistForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})



class AddProfessionalServiceForm(ModelForm):
    class Meta:
        model = Professional_Service_Information
        # fields = ['name','address','featured_image','phone_number','email','profession']
        fields = ['name','profession']

    def __init__(self, *args, **kwargs):
        super(AddProfessionalServiceForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class EditProfessionalServiceForm(forms.ModelForm):
    class Meta:
        model = Professional_Service_Information
        # fields = ['name','address','featured_image','phone_number','email','profession']
        fields = ['name','profession', 'featured_image']

    def __init__(self, *args, **kwargs):
        super(EditProfessionalServiceForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class EditEmergencyForm(forms.ModelForm):
    class Meta:
        model = Professional_Service_Information
        # fields = ['general_bed_no','available_icu_no','regular_cabin_no','emergency_cabin_no','vip_cabin_no']
        fields = []

    def __init__(self, *args, **kwargs):
        super(EditEmergencyForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class AddEmergencyForm(ModelForm):
    class Meta:
        model = Professional_Service_Information
        # fields = ['name','general_bed_no','available_icu_no','regular_cabin_no','emergency_cabin_no','vip_cabin_no']
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(AddEmergencyForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class AdminForm(ModelForm):
    class Meta:
        model = Admin_Information
        fields = ['name', 'email', 'phone_number', 'role','featured_image']

    def __init__(self, *args, **kwargs):
         super(AdminForm, self).__init__(*args, **kwargs)

         for name, field in self.fields.items():
             field.widget.attrs.update({'class': 'form-control'})

