import email
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ClientForm, PasswordResetForm
from service_provider.models import Service_Provider_Information, User, Client 
from professional.models import Test, testCart, testOrder
from service_provider_admin.models import ServiceDepartment, specialization, service, Test_Information
from django.views.decorators.cache import cache_control
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import datetime
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import searchProfessionals, searchServiceProviders, searchDepartmentProfessionals, paginateServiceProviders
from .models import Client, User
from professional.models import Professional_Information, Appointment,Report, Specimen, Test, Prescription, Prescription_product, Prescription_test
from sslcommerz.models import Payment
from django.db.models import Q, Count
import re
from io import BytesIO
from urllib import response
from django.core.mail import BadHeaderError, send_mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def service_provider_home(request):
    # .order_by('-created_at')[:6]
    professionals = Professional_Information.objects.filter(register_status='Accepted')
    service_providers = Service_Provider_Information.objects.all()
    context = {'professionals': professionals, 'service_providers': service_providers} 
    return render(request, 'index-2.html', context)

@csrf_exempt
@login_required(login_url="login")
def change_password(request,pk):
    client = Client.objects.get(user_id=pk)
    context={"client":client}
    if request.method == "POST":
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]
        if new_password == confirm_password:
            
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request,"Password Changed Successfully")
            return redirect("client-dashboard")
        else:
            messages.error(request,"New Password and Confirm Password is not same")
            return redirect("change-password",pk)
    return render(request, 'change-password.html',context)


def add_billing(request):
    return render(request, 'add-billing.html')

def appointments(request):
    return render(request, 'appointments.html')

def edit_billing(request):
    return render(request, 'edit-billing.html')

def edit_prescription(request):
    return render(request, 'edit-prescription.html')

# def forgot_password(request):
#     return render(request, 'forgot-password.html')

@csrf_exempt
def resetPassword(request):
    form = PasswordResetForm()

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = user.email
       
            subject = "Password Reset Requested"
            # email_template_name = "password_reset_email.txt"
            values = {
				"email":user.email,
				'domain':'127.0.0.1:8000',
				'site_name': 'Website',
				"uid": urlsafe_base64_encode(force_bytes(user.pk)),
				"user": user,
				'token': default_token_generator.make_token(user),
				'protocol': 'http',
			}

            html_message = render_to_string('mail_template.html', {'values': values})
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(subject, plain_message, 'admin@example.com',  [user.email], html_message=html_message, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect ("password_reset_done")

    context = {'form': form}
    return render(request, 'reset_password.html', context)
    
    
def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def about_us(request):
    return render(request, 'about-us.html')

@csrf_exempt
@login_required(login_url="login")
def chat(request, pk):
    client = Client.objects.get(user_id=pk)
    professionals = Professional_Information.objects.all()

    context = {'client': client, 'professionals': professionals}
    return render(request, 'chat.html', context)

@csrf_exempt
@login_required(login_url="login")
def chat_professional(request):
    if request.user.is_professional:
        professional = Professional_Information.objects.get(user=request.user)
        clients = Client.objects.all()
        
    context = {'clients': clients, 'professional': professional}
    return render(request, 'chat-professional.html', context)

@csrf_exempt     
@login_required(login_url="login")
def pharmacy_shop(request):
    return render(request, 'pharmacy/shop.html')

@csrf_exempt
def login_user(request):
    page = 'client_login'
    if request.method == 'GET':
        return render(request, 'client-login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_client:   
                messages.success(request, 'User Logged in Successfully')    
                return redirect('client-dashboard')
            else:
                messages.error(request, 'Invalid credentials. Not a Client')
                return redirect('logout')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'client-login.html')

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
    logout(request)
    messages.success(request, 'User Logged out')
    return redirect('login')

@csrf_exempt
def client_register(request):
    page = 'client-register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save(commit=False) # commit=False --> don't save to database yet (we have a chance to modify object)
            user.is_client = True
            # user.username = user.username.lower()  # lowercase username
            user.save()
            messages.success(request, 'Client account was created!')

            # After user is created, we can log them in --> login(request, user)
            return redirect('login')

        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'client-register.html', context)

@csrf_exempt
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def client_dashboard(request):
    if request.user.is_client:
        # client = Client.objects.get(user_id=pk)
        client = Client.objects.get(user=request.user)
        # report = Report.objects.filter(client=client)
        # prescription = Prescription.objects.filter(client=client).order_by('-prescription_id')
        appointments = Appointment.objects.filter(client=client).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed'))
        # payments = Payment.objects.filter(client=client).filter(appointment__in=appointments).filter(payment_type='appointment').filter(status='VALID')
        # context = {'client': client, 'appointments': appointments, 'payments': payments,'report':report,'prescription':prescription}
        context = {'client': client, 'appointments': appointments}
    else:
        return redirect('logout')
        
    return render(request, 'client-dashboard.html', context)


# def profile_settings(request):
#     if request.user.is_patient:
#         # patient = Client.objects.get(user_id=pk)
#         patient = Client.objects.get(user=request.user)
#         form = ClientForm(instance=patient)  

#         if request.method == 'POST':
#             form = ClientForm(request.POST, request.FILES,instance=patient)  
#             if form.is_valid():
#                 form.save()
#                 return redirect('patient-dashboard')
#             else:
#                 form = ClientForm()
#     else:
#         redirect('logout')

#     context = {'patient': patient, 'form': form}
#     return render(request, 'profile-settings.html', context)

@csrf_exempt
@login_required(login_url="login")
def profile_settings(request):
    if request.user.is_client:
        # patient = Client.objects.get(user_id=pk)
        client = Client.objects.get(user=request.user)
        old_featured_image = client.featured_image
        
        if request.method == 'GET':
            context = {'client': client}
            return render(request, 'profile-settings.html', context)
        elif request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = old_featured_image
                
            name = request.POST.get('name')
            # dob = request.POST.get('dob')
            age = request.POST.get('age')
            # blood_group = request.POST.get('blood_group')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            # nid = request.POST.get('nid')
            history = request.POST.get('history')
            
            client.name = name
            client.age = age
            client.phone_number = phone_number
            client.address = address
            # client.blood_group = blood_group
            client.history = history
            # client.dob = dob
            # client.nid = nid
            client.featured_image = featured_image
            
            client.save()
            
            messages.success(request, 'Profile Settings Changed!')
            
            return redirect('client-dashboard')
    else:
        redirect('logout')  
        
@csrf_exempt
@login_required(login_url="login")
def search(request):
    if request.user.is_authenticated and request.user.is_client:
        # patient = Client.objects.get(user_id=pk)
        client = Client.objects.get(user=request.user)
        professionals = Professional_Information.objects.filter(register_status='Accepted')
        
        professionals, search_query = searchProfessionals(request)
        context = {'client': client, 'professionals': professionals, 'search_query': search_query}
        return render(request, 'search.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')    
    

def checkout_payment(request):
    return render(request, 'checkout.html')

@csrf_exempt
@login_required(login_url="login")
def multiple_service_provider(request):
    
    if request.user.is_authenticated: 
        
        if request.user.is_client:
            # client = Client.objects.get(user_id=pk)
            client = Client.objects.get(user=request.user)
            professionals = Professional_Information.objects.all()
            service_providers = Service_Provider_Information.objects.all()
            
            service_providers, search_query = searchServiceProviders(request)
            
            # PAGINATION ADDED TO MULTIPLE HOSPITALS
            custom_range, service_providers = paginateServiceProviders(request, service_providers, 3)
        
            context = {'client': client, 'professionals': professionals, 'service_providers': service_providers, 'search_query': search_query, 'custom_range': custom_range}
            return render(request, 'multiple-service_provider.html', context)
        
        elif request.user.is_professional:
            professional = Professional_Information.objects.get(user=request.user)
            service_providers = Service_Provider_Information.objects.all()
            
            service_providers, search_query = searchServiceProviders(request)
            
            context = {'professional': professional, 'service_providers': service_providers, 'search_query': search_query}
            return render(request, 'multiple-service_provider.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html') 
    
@csrf_exempt    
@login_required(login_url="login")
def service_provider_profile(request, pk):
    
    if request.user.is_authenticated: 
        
        if request.user.is_client:
            client = Client.objects.get(user=request.user)
            professionals = Professional_Information.objects.all()
            service_providers = Service_Provider_Information.objects.get(service_provider_id=pk)
        
            professions = ServiceDepartment.objects.filter(service_provider=service_providers)
            specializations = specialization.objects.filter(service_provider=service_providers)
            services = service.objects.filter(service_provider=service_providers)
            
            # department_list = None
            # for d in departments:
            #     vald = d.hospital_department_name
            #     vald = re.sub("'", "", vald)
            #     vald = vald.replace("[", "")
            #     vald = vald.replace("]", "")
            #     vald = vald.replace(",", "")
            #     department_list = vald.split()
            
            context = {'client': client, 'professionals': professionals, 'service_providers': service_providers, 'professions': professions, 'specializations': specializations, 'services': services}
            return render(request, 'service_provider-profile.html', context)
        
        elif request.user.is_professional:
           
            professional = Professional_Information.objects.get(user=request.user)
            service_providers = Service_Provider_Information.objects.get(service_provider_id=pk)
            
            professions = ServiceDepartment.objects.filter(service_provider=service_providers)
            specializations = specialization.objects.filter(service_provider=service_providers)
            services = service.objects.filter(service_provider=service_providers)
            
            context = {'professional': professional, 'service_providers': service_providers, 'professions': professions, 'specializations': specializations, 'services': services}
            return render(request, 'service_provider-profile.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html') 
    
    
def data_table(request):
    return render(request, 'data-table.html')

@csrf_exempt
@login_required(login_url="login")
def ServiceType_list(request, pk):
    if request.user.is_authenticated: 
        
        if request.user.is_client:
            # patient = Client.objects.get(user_id=pk)
            client = Client.objects.get(user=request.user)
            professionals = Professional_Information.objects.all()
            
            service_providers = Service_Provider_Information.objects.get(service_provider_id=pk)
            professions = ServiceDepartment.objects.filter(service_provider=service_providers)
        
            context = {'client': client, 'professionals': professionals, 'service_providers': service_providers, 'professions': professions}
            return render(request, 'service_provider-profession-list.html', context)
        
        elif request.user.is_professional:
            professional = Professional_Information.objects.get(user=request.user)
            service_providers = Service_Provider_Information.objects.get(service_provider_id=pk)
            professions = ServiceDepartment.objects.filter(service_provider=service_providers)
            
            context = {'professional': professional, 'service_providers': service_providers, 'professions': professions}
            return render(request, 'service_provider-profession-list.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'client-login.html')

@csrf_exempt
@login_required(login_url="login")
def service_provider_professional_list(request, pk):
    if request.user.is_authenticated and request.user.is_client:
        # patient = Client.objects.get(user_id=pk)
        client = Client.objects.get(user=request.user)
        professions = ServiceDepartment.objects.get(ServiceDepartment_id=pk)
        professionals = Professional_Information.objects.filter(profession_name=professions)
        
        professionals, search_query = searchDepartmentProfessionals(request, pk)
        
        context = {'client': client, 'profession': professions, 'professionals': professionals, 'search_query': search_query, 'pk_id': pk}
        return render(request, 'service_provider-professional-list.html', context)

    elif request.user.is_authenticated and request.user.is_professional:
        # patient = Client.objects.get(user_id=pk)
        
        professional = Professional_Information.objects.get(user=request.user)
        professions = ServiceDepartment.objects.get(ServiceDepartment_id=pk)
        
        professionals = Professional_Information.objects.filter(profession_name=professions)
        professionals, search_query = searchDepartmentProfessionals(request, pk)
        
        context = {'professional':professional, 'profession': professions, 'professionals': professionals, 'search_query': search_query, 'pk_id': pk}
        return render(request, 'service_provider-professional-list.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')   
    


@csrf_exempt
@login_required(login_url="login")
def service_provider_professional_register(request, pk):
    if request.user.is_authenticated: 
        
        if request.user.is_professional:
            professional = Professional_Information.objects.get(user=request.user)
            service_providers = Service_Provider_Information.objects.get(service_provider_id=pk)
            
            professions = ServiceDepartment.objects.filter(service_provider=service_providers)
            specializations = specialization.objects.filter(service_provider=service_providers)
            
            if request.method == 'POST':
                if 'certificate_image' in request.FILES:
                    certificate_image = request.FILES['certificate_image']
                else:
                    certificate_image = "professionals_certificate/default.png"
                
                profession_id_selected = request.POST.get('profession_radio')
                specialization_id_selected = request.POST.get('specialization_radio')
                
                profession_chosen = ServiceDepartment.objects.get(ServiceDepartment_id=profession_id_selected)
                specialization_chosen = specialization.objects.get(specialization_id=specialization_id_selected)
                
                professional.profession_name = profession_chosen
                professional.specialization = specialization_chosen
                professional.register_status = 'Pending'
                professional.certificate_image = certificate_image
                
                professional.save()
                
                messages.success(request, 'ServiceProvider Registration Request Sent')
                
                return redirect('professional-dashboard')
                
                 
            context = {'professional': professional, 'service_providers': service_providers, 'professions': professions, 'specializations': specializations}
            return render(request, 'service_provider-professional-register.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'professional-login.html')
    
   
def testing(request):
    # service_providers = Service_Provider_Information.objects.get(service_provider_id=1)
    test = "test"
    context = {'test': test}
    return render(request, 'testing.html', context)

@csrf_exempt
@login_required(login_url="login")
def view_report(request,pk):
    if request.user.is_client:
        client = Client.objects.get(user=request.user)
        report = Report.objects.filter(report_id=pk)
        specimen = Specimen.objects.filter(report__in=report)
        test = Test.objects.filter(report__in=report)

        # current_date = datetime.date.today()
        context = {'client':client,'report':report,'test':test,'specimen':specimen}
        return render(request, 'view-report.html',context)
    else:
        redirect('logout') 


def test_cart(request):
    return render(request, 'test-cart.html')

@csrf_exempt
@login_required(login_url="login")
def test_single(request,pk):
     if request.user.is_authenticated and request.user.is_client:
         
        client = Client.objects.get(user=request.user)
        Perscription_test = Perscription_test.objects.get(test_id=pk)
        carts = testCart.objects.filter(user=request.user, purchased=False)
        
        context = {'client': client, 'carts': carts, 'Perscription_test': Perscription_test}
        return render(request, 'test-cart.html',context)
     else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'client-login.html')  

@csrf_exempt
@login_required(login_url="login")
def test_add_to_cart(request, pk, pk2):
    if request.user.is_authenticated and request.user.is_client:
         
        client = Client.objects.get(user=request.user)
        test_information = Test_Information.objects.get(test_id=pk2)
        prescription = Prescription.objects.filter(prescription_id=pk)

        item = get_object_or_404(Prescription_test, test_info_id=pk2,prescription_id=pk)
        order_item = testCart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = testOrder.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            order.orderitems.add(order_item[0])
            # messages.info(request, "This test is added to your cart!")
            return redirect("prescription-view", pk=pk)
        else:
            order = testOrder(user=request.user)
            order.save()
            order.orderitems.add(order_item[0])
            return redirect("prescription-view", pk=pk)

        context = {'client': client,'prescription_test': prescription_tests,'prescription':prescription,'prescription_product':prescription_product,'test_information':test_information}
        return render(request, 'prescription-view.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'client-login.html')  

@csrf_exempt
@login_required(login_url="login")
def test_cart(request, pk):
    if request.user.is_authenticated and request.user.is_client:
        # prescription = Prescription.objects.filter(prescription_id=pk)
        
        prescription = Prescription.objects.filter(prescription_id=pk)
        
        client = Client.objects.get(user=request.user)
        prescription_test = Prescription_test.objects.all()
        test_carts = testCart.objects.filter(user=request.user, purchased=False)
        test_orders = testOrder.objects.filter(user=request.user, ordered=False)
        
        if test_carts.exists() and test_orders.exists():
            test_order = test_orders[0]
            
            context = {'test_carts': test_carts,'test_order': test_order, 'client': client, 'prescription_test':prescription_test, 'prescription_id':pk}
            return render(request, 'test-cart.html', context)
        else:
            # messages.warning(request, "You don't have any test in your cart!")
            context = {'client': client,'prescription_test':prescription_test}
            return render(request, 'prescription-view.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'client-login.html') 

@csrf_exempt
@login_required(login_url="login")
def test_remove_cart(request, pk):
    if request.user.is_authenticated and request.user.is_client:
        item = Prescription_test.objects.get(test_id=pk)

        client = Client.objects.get(user=request.user)
        prescription = Prescription.objects.filter(prescription_id=pk)
        prescription_product = Prescription_product.objects.filter(prescription__in=prescription)
        prescription_test = Prescription_test.objects.filter(prescription__in=prescription)
        test_carts = testCart.objects.filter(user=request.user, purchased=False)
        
        # item = get_object_or_404(test, pk=pk)
        test_order_qs = testOrder.objects.filter(user=request.user, ordered=False)
        if test_order_qs.exists():
            test_order = test_order_qs[0]
            if test_order.orderitems.filter(item=item).exists():
                test_order_item = testCart.objects.filter(item=item, user=request.user, purchased=False)[0]
                test_order.orderitems.remove(test_order_item)
                test_order_item.delete()
                # messages.warning(request, "This test was remove from your cart!")
                context = {'test_carts': test_carts,'test_order': test_order,'client': client,'prescription_id':pk}
                return render(request, 'test-cart.html', context)
            else:
                # messages.info(request, "This test was not in your cart")
                context = {'client': client,'test': item,'prescription':prescription,'prescription_product':prescription_product,'prescription_test':prescription_test}
                return render(request, 'prescription-view.html', context)
        else:
            # messages.info(request, "You don't have an active order")
            context = {'client': client,'test': item,'prescription':prescription,'prescription_product':prescription_product,'prescription_test':prescription_test}
            return redirect('prescription-view', pk=prescription.prescription_id)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'client-login.html') 

@csrf_exempt
def prescription_view(request,pk):
      if request.user.is_client:
        client = Client.objects.get(user=request.user)
        prescription = Prescription.objects.filter(prescription_id=pk)
        prescription_product = Prescription_product.objects.filter(prescription__in=prescription)
        prescription_test = Prescription_test.objects.filter(prescription__in=prescription)

        context = {'client':client,'prescription':prescription,'prescription_test':prescription_test,'prescription_product':prescription_product}
        return render(request, 'prescription-view.html',context)
      else:
         redirect('logout') 

@csrf_exempt
def render_to_pdf(template_src, context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pres_pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pres_pdf.err:
        return HttpResponse(result.getvalue(),content_type="aplication/pres_pdf")
    return None


# def prescription_pdf(request,pk):
#  if request.user.is_patient:
#     patient = Client.objects.get(user=request.user)
#     prescription = Prescription.objects.get(prescription_id=pk)
#     perscription_medicine = Perscription_medicine.objects.filter(prescription=prescription)
#     perscription_test = Perscription_test.objects.filter(prescription=prescription)
#     current_date = datetime.date.today()
#     context={'patient':patient,'current_date' : current_date,'prescription':prescription,'perscription_test':perscription_test,'perscription_medicine':perscription_medicine}
#     pdf=render_to_pdf('prescription_pdf.html', context)
#     if pdf:
#         response=HttpResponse(pdf, content_type='application/pdf')
#         content="inline; filename=report.pdf"
#         # response['Content-Disposition']= content
#         return response
#     return HttpResponse("Not Found")

@csrf_exempt
def prescription_pdf(request,pk):
 if request.user.is_client:
    client = Client.objects.get(user=request.user)
    prescription = Prescription.objects.get(prescription_id=pk)
    prescription_product = Prescription_product.objects.filter(prescription=prescription)
    prescription_test = Prescription_test.objects.filter(prescription=prescription)
    # current_date = datetime.date.today()
    context={'client':client,'prescription':prescription,'prescription_test':prescription_test,'prescription_product':prescription_product}
    pres_pdf=render_to_pdf('prescription_pdf.html', context)
    if pres_pdf:
        response=HttpResponse(pres_pdf, content_type='application/pres_pdf')
        content="inline; filename=prescription.pdf"
        response['Content-Disposition']= content
        return response
    return HttpResponse("Not Found")

@csrf_exempt
@login_required(login_url="login")
def delete_prescription(request,pk):
    if request.user.is_authenticated and request.user.is_client:
        prescription = Prescription.objects.get(prescription_id=pk)
        prescription.delete()
        messages.success(request, 'Prescription Deleted')
        return redirect('client-dashboard')
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')

@csrf_exempt
@login_required(login_url="login")
def delete_report(request,pk):
    if request.user.is_authenticated and request.user.is_client:
        report = Report.objects.get(report_id=pk)
        report.delete()
        messages.success(request, 'Report Deleted')
        return redirect('client-dashboard')
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')

@csrf_exempt
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.login_status = True
    user.save()

@csrf_exempt
@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.login_status = False
    user.save()
    


