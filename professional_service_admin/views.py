import email
from email.mime import image
from multiprocessing import context
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from professional_service.models import Professional_Service_Information, User, Client
from django.db.models import Q
from store.models import Product, StoreManager
from professional.models import Professional_Information, ServiceRequest, ServiceRequest_test, Report, Appointment, Experience , Education,Specimen,Test
from store.models import ServiceOrder, Cart
from sslcommerz.models import Payment
from .forms import AdminUserCreationForm, TechnicalSpecialistCreationForm, EditProfessionalServiceForm, EditEmergencyForm,AdminForm , StoreManagerCreationForm 

from .models import Admin_Information,specialization,service,ServiceDepartment, Clinical_Laboratory_Technician, Test_Information
import random,re
import string
from django.db.models import  Count
from datetime import datetime
import datetime
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.html import strip_tags
from .utils import searchProducts

# Create your views here.

@csrf_exempt
@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    # admin = Admin_Information.objects.get(user_id=pk)
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        total_client_count = Client.objects.annotate(count=Count('client_id'))
        total_professional_count = Professional_Information.objects.annotate(count=Count('professional_id'))
        total_storeManager_count = StoreManager.objects.annotate(count=Count('storeManager_id'))
        total_professional_service_count = Professional_Service_Information.objects.annotate(count=Count('professional_service_id'))
        total_technicalSpecialist_count = Clinical_Laboratory_Technician.objects.annotate(count=Count('technician_id'))
        pending_appointment = Appointment.objects.filter(appointment_status='pending').count()
        professionals = Professional_Information.objects.all()
        clients = Client.objects.all()
        professional_services = Professional_Service_Information.objects.all()
        technical_specialists = Clinical_Laboratory_Technician.objects.all()
        storeManagers = StoreManager.objects.all()
        
        sat_date = datetime.date.today()
        sat_date_str = str(sat_date)
        sat = sat_date.strftime("%A")

        sun_date = sat_date + datetime.timedelta(days=1) 
        sun_date_str = str(sun_date)
        sun = sun_date.strftime("%A")
        
        mon_date = sat_date + datetime.timedelta(days=2) 
        mon_date_str = str(mon_date)
        mon = mon_date.strftime("%A")
        
        tues_date = sat_date + datetime.timedelta(days=3) 
        tues_date_str = str(tues_date)
        tues = tues_date.strftime("%A")
        
        wed_date = sat_date + datetime.timedelta(days=4) 
        wed_date_str = str(wed_date)
        wed = wed_date.strftime("%A")
        
        thurs_date = sat_date + datetime.timedelta(days=5) 
        thurs_date_str = str(thurs_date)
        thurs = thurs_date.strftime("%A")
        
        fri_date = sat_date + datetime.timedelta(days=6) 
        fri_date_str = str(fri_date)
        fri = fri_date.strftime("%A")
        
        sat_count = Appointment.objects.filter(date=sat_date_str).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed')).count()
        sun_count = Appointment.objects.filter(date=sun_date_str).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed')).count()
        mon_count = Appointment.objects.filter(date=mon_date_str).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed')).count()
        tues_count = Appointment.objects.filter(date=tues_date_str).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed')).count()
        wed_count = Appointment.objects.filter(date=wed_date_str).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed')).count()
        thurs_count = Appointment.objects.filter(date=thurs_date_str).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed')).count()
        fri_count = Appointment.objects.filter(date=fri_date_str).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed')).count()

        context = {'admin': user,'total_client_count': total_client_count,'total_professional_count':total_professional_count,'pending_appointment':pending_appointment,'professionals':professionals,'clients':clients,'professional_services':professional_services,'technical_specialists':technical_specialists,'total_storeManager_count':total_storeManager_count,'total_professional_service_count':total_professional_service_count,'total_technicalSpecialist_count':total_technicalSpecialist_count,'sat_count': sat_count, 'sun_count': sun_count, 'mon_count': mon_count, 'tues_count': tues_count, 'wed_count': wed_count, 'thurs_count': thurs_count, 'fri_count': fri_count, 'sat': sat, 'sun': sun, 'mon': mon, 'tues': tues, 'wed': wed, 'thurs': thurs, 'fri': fri, 'storeManagers': storeManagers}
        return render(request, 'professional_service_admin/admin-dashboard.html', context)
    elif request.user.is_technicalSpecialist:
        # messages.error(request, 'You are not authorized to access this page')
        return redirect('technicalSpecialist-dashboard')
    # return render(request, 'professional_service_admin/admin-dashboard.html', context)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutAdmin(request):
    logout(request)
    messages.error(request, 'User Logged out')
    return redirect('admin_login')
            
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.method == 'GET':
        return render(request, 'professional_service_admin/login.html')
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
            if user.is_professional_service_admin:
                messages.success(request, 'User logged in')
                return redirect('admin-dashboard')
            elif user.is_technicalSpecialist:
                messages.success(request, 'User logged in')
                return redirect('technicalSpecialist-dashboard')
            elif user.is_storeManager:
                messages.success(request, 'User logged in')
                return redirect('storeManager-dashboard')
            else:
                return redirect('admin-logout')
        else:
            messages.error(request, 'Invalid username or password')
        

    return render(request, 'professional_service_admin/login.html')


@csrf_exempt
def admin_register(request):
    page = 'professional_service_admin/register'
    form = AdminUserCreationForm()

    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            # commit=False --> don't save to database yet (we have a chance to modify object)
            user = form.save(commit=False)
            user.is_professional_service_admin = True
            user.save()

            messages.success(request, 'User account was created!')
            
            # After user is created, we can log them in
            #login(request, user)
            return redirect('admin_login')

        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'professional_service_admin/register.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def admin_forgot_password(request):
    return render(request, 'professional_service_admin/forgot-password.html')

@csrf_exempt
@login_required(login_url='admin_login')
def invoice(request):
    return render(request, 'professional_service_admin/invoice.html')

@csrf_exempt
@login_required(login_url='admin_login')
def invoice_report(request):
    return render(request, 'professional_service_admin/invoice-report.html')

@login_required(login_url='admin_login')
def lock_screen(request):
    return render(request, 'professional_service_admin/lock-screen.html')

@csrf_exempt
@login_required(login_url='admin_login')
def client_list(request):
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
    clients = Client.objects.all()
    return render(request, 'professional_service_admin/client-list.html', {'all': clients, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def specialitites(request):
    return render(request, 'professional_service_admin/specialities.html')

@csrf_exempt
@login_required(login_url='admin_login')
def appointment_list(request):
    return render(request, 'professional_service_admin/appointment-list.html')

@login_required(login_url='admin_login')
def transactions_list(request):
    return render(request, 'professional_service_admin/transactions-list.html')

@csrf_exempt
@login_required(login_url='admin_login')
def emergency_details(request):
    user = Admin_Information.objects.get(user=request.user)
    professional_services = Professional_Service_Information.objects.all()
    context = { 'admin': user, 'all': professional_services}
    return render(request, 'professional_service_admin/emergency.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def professional_service_list(request):
    user = Admin_Information.objects.get(user=request.user)
    professional_services = Professional_Service_Information.objects.all()
    context = { 'admin': user, 'professional_services': professional_services}
    return render(request, 'professional_service_admin/professional_service-list.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def appointment_list(request):
    return render(request, 'professional_service_admin/appointment-list.html')

@csrf_exempt
@login_required(login_url='admin_login')
def professional_service_profile(request):
    return render(request, 'professional_service-profile.html')

@csrf_exempt
@login_required(login_url='admin_login')
def professional_service_admin_profile(request, pk):

    # profile = request.user.profile
    # get user id of logged in user, and get all info from table
    admin = Admin_Information.objects.get(user_id=pk)
    form = AdminForm(instance=admin)

    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES,
                          instance=admin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated')
            return redirect('admin-dashboard', pk=pk)
        else:
            form = AdminForm()

    context = {'admin': admin, 'form': form}
    return render(request, 'professional_service_admin/professional_service-admin-profile.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def add_professional_service(request):
    if  request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)

        if request.method == 'POST':
            professional_service = Professional_Service_Information()
            
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = "professions/default.png"
            
            service_name = request.POST.get('service_name')
            address = request.POST.get('address')
            description = request.POST.get('description')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number') 
            profession = request.POST.get('type')
            specialization_name = request.POST.getlist('specialization')
            profession_name = request.POST.getlist('profession')
            service_name = request.POST.getlist('service')
            
        
            professional_service.name = service_name
            professional_service.description = description
            professional_service.address = address
            professional_service.email = email
            professional_service.phone_number =phone_number
            professional_service.featured_image=featured_image 
            professional_service.profession=profession
            
            # print(department_name[0])
         
            professional_service.save()
            
            for i in range(len(profession_name)):
                professions = ServiceDepartment(professional_service=professional_service)
                # print(department_name[i])
                professions.ServiceDepartment_name = profession_name[i]
                professions.save()
                
            for i in range(len(specialization_name)):
                specializations = specialization(professional_service=professional_service)
                specializations.specialization_name=specialization_name[i]
                specializations.save()
                
            for i in range(len(service_name)):
                services = service(professional_service=professional_service)
                services.service_name = service_name[i]
                services.save()
            
            messages.success(request, 'Professional Service Added')
            return redirect('professional_service-list')

        context = { 'admin': user}
        return render(request, 'professional_service_admin/add-professional_service.html',context)


# def edit_hospital(request, pk):
#     hospital = Hospital_Information.objects.get(hospital_id=pk)
#     return render(request, 'professional_service_admin/edit-hospital.html')

@csrf_exempt
@login_required(login_url='admin_login')
def edit_professional_service(request, pk):
    if  request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        professional_service = Professional_Service_Information.objects.get(professional_service_id=pk)
        old_featured_image = professional_service.featured_image

        if request.method == 'GET':
            specializations = specialization.objects.filter(professional_service=professional_service)
            services = service.objects.filter(professional_service=professional_service)
            professions = ServiceDepartment.objects.filter(professional_service=professional_service)
            context = {'professional_service': professional_service, 'specializations': specializations, 'services': services,'professions':professions, 'admin': user}
            return render(request, 'professional_service_admin/edit-professional_service.html',context)

        elif request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = old_featured_image
                               
            service_name = request.POST.get('service_name')
            address = request.POST.get('address')
            description = request.POST.get('description')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number') 
            profession = request.POST.get('type')
            
            specialization_name = request.POST.getlist('specialization')
            profession_name = request.POST.getlist('profession')
            service_name = request.POST.getlist('service')

            professional_service.name = service_name
            professional_service.description = description
            professional_service.address = address
            professional_service.email = email
            professional_service.phone_number =phone_number
            professional_service.featured_image =featured_image 
            professional_service.profession =profession
            
            # specializations.specialization_name=specialization_name
            # services.service_name = service_name
            # departments.ServiceDepartment_name = department_name 

            professional_service.save()

            # Specialization
            for i in range(len(specialization_name)):
                specializations = specialization(professional_service=professional_service)
                specializations.specialization_name = specialization_name[i]
                specializations.save()

            # Experience
            for i in range(len(service_name)):
                services = service(professional_service=professional_service)
                services.service_name = service_name[i]
                services.save()
                
            for i in range(len(profession_name)):
                professions = ServiceDepartment(professional_service=professional_service)
                professions.ServiceDepartment_name = profession_name[i]
                professions.save()

            messages.success(request, 'Professional Service Updated')
            return redirect('professional_service-list')

@csrf_exempt
@login_required(login_url='admin_login')
def delete_specialization(request, pk, pk2):
    specializations = specialization.objects.get(specialization_id=pk)
    specializations.delete()
    messages.success(request, 'Delete Specialization')
    return redirect('edit-professional_service', pk2)

@csrf_exempt
@login_required(login_url='admin_login')
def delete_service(request, pk, pk2):
    services = service.objects.get(service_id=pk)
    services.delete()
    messages.success(request, 'Delete Service')
    return redirect('edit-professional_service', pk2)

@csrf_exempt
@login_required(login_url='admin_login')
def edit_emergency_information(request, pk):

    professional_service = Professional_Service_Information.objects.get(professional_service_id=pk)
    form = EditEmergencyForm(instance=professional_service)  

    if request.method == 'POST':
        form = EditEmergencyForm(request.POST, request.FILES,
                           instance=professional_service)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Emergency information added')
            return redirect('emergency')
        else:
            form = EditEmergencyForm()

    context = {'professional_service': professional_service, 'form': form}
    return render(request, 'professional_service_admin/edit-emergency-information.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def delete_professional_service(request, pk):
	professional_service = Professional_Service_Information.objects.get(professional_service_id=pk)
	professional_service.delete()
	return redirect('professional_service-list')


@login_required(login_url='admin_login')
def generate_random_invoice():
    N = 4
    string_var = ""
    string_var = ''.join(random.choices(string.digits, k=N))
    string_var = "#INV-" + string_var
    return string_var

@csrf_exempt
@login_required(login_url='admin_login')
def create_invoice(request, pk):
    if  request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)

    client = Client.objects.get(client_id=pk)

    if request.method == 'POST':
        invoice = Payment(client=client)
        
        consulation_fee = request.POST['consulation_fee']
        services_fee = request.POST['services_fee']
        #total_ammount = request.POST['currency_amount']
        invoice.currency_amount = int(consulation_fee) + int(services_fee)
        invoice.consulation_fee = consulation_fee
        invoice.services_fee = services_fee
        invoice.invoice_number = generate_random_invoice()
        invoice.name = client
        invoice.status = 'Pending'
    
        invoice.save()
        return redirect('client-list')

    context = {'client': client,'admin': user}
    return render(request, 'professional_service_admin/create-invoice.html', context)


@login_required(login_url='admin_login')
def generate_random_specimen():
    N = 4
    string_var = ""
    string_var = ''.join(random.choices(string.digits, k=N))
    string_var = "#INV-" + string_var
    return string_var

@login_required(login_url='admin-login')
@csrf_exempt
def create_report(request, pk):
    if request.user.is_technicalSpecialist:
        technical_specialists = Clinical_Laboratory_Technician.objects.get(user=request.user)
        serviceRequest =ServiceRequest.objects.get(serviceRequest_id=pk)
        client = Client.objects.get(client_id=serviceRequest.client_id)
        professional = Professional_Information.objects.get(professional_id=serviceRequest.professional_id)
        tests = ServiceRequest_test.objects.filter(serviceRequest=serviceRequest).filter(test_info_pay_status='Paid')
        

        if request.method == 'POST':
            report = Report(professional=professional, client=client)
            
            specimen_type = request.POST.getlist('specimen_type')
            collection_date  = request.POST.getlist('collection_date')
            receiving_date = request.POST.getlist('receiving_date')
            test_name = request.POST.getlist('test_name')
            result = request.POST.getlist('result')
            unit = request.POST.getlist('unit')
            referred_value = request.POST.getlist('referred_value')
            delivery_date = request.POST.get('delivery_date')
            other_information= request.POST.get('other_information')

            # # Save to report table
            # report.test_name = test_name
            # report.result = result
            report.delivery_date = delivery_date
            report.other_information = other_information
            # #report.specimen_id =generate_random_specimen()
            # report.specimen_type = specimen_type
            # report.collection_date  = collection_date 
            # report.receiving_date = receiving_date
            # report.unit = unit
            # report.referred_value = referred_value

            report.save()

            for i in range(len(specimen_type)):
                specimens = Specimen(report=report)
                specimens.specimen_type = specimen_type[i]
                specimens.collection_date = collection_date[i]
                specimens.receiving_date = receiving_date[i]
                specimens.save()
                
            for i in range(len(test_name)):
                tests = Test(report=report)
                tests.test_name=test_name[i]
                tests.result=result[i]
                tests.unit=unit[i]
                tests.referred_value=referred_value[i]
                tests.save()
            
            # mail
            professional_name = professional.name
            professional_email = professional.email
            client_name = client.name
            client_email = client.email
            report_id = report.report_id
            delivery_date = report.delivery_date
            
            subject = "Report Delivery"

            values = {
                    "professional_name":professional_name,
                    "professional_email":professional_email,
                    "client_name":client_name,
                    "report_id":report_id,
                    "delivery_date":delivery_date,
                }

            html_message = render_to_string('professional_service_admin/report-mail-delivery.html', {'values': values})
            plain_message = strip_tags(html_message)

            try:
                send_mail(subject, plain_message, 'professional_service_admin@gmail.com',  [client_email], html_message=html_message, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found') 

            return redirect('myclientlist')

        context = {'serviceRequest':serviceRequest,'technical_specialists':technical_specialists,'tests':tests}
        return render(request, 'professional_service_admin/create-report.html',context)

@csrf_exempt
@login_required(login_url='admin_login')
def add_storeManager(request):
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        form = StoreManagerCreationForm()
     
        if request.method == 'POST':
            form = StoreManagerCreationForm(request.POST)
            if form.is_valid():
                # form.save(), commit=False --> don't save to database yet (we have a chance to modify object)
                user = form.save(commit=False)
                user.is_storeManager = True
                user.save()

                messages.success(request, 'StoreManager account was created!')

                # After user is created, we can log them in
                #login(request, user)
                return redirect('storeManager-list')
            else:
                messages.error(request, 'An error has occurred during registration')
    
    context = {'form': form, 'admin': user}
    return render(request, 'professional_service_admin/add-storeManager.html', context)
  
@csrf_exempt
@login_required(login_url='admin_login')
def product_list(request):
    if request.user.is_authenticated:
        if request.user.is_storeManager:
            storeManager = StoreManager.objects.get(user=request.user)
            product = Product.objects.all()
            orders = ServiceOrder.objects.filter(user=request.user, ordered=False)
            carts = Cart.objects.filter(user=request.user, purchased=False)
            
            product, search_query = searchProduct(request)
            
            if carts.exists() and orders.exists():
                order = orders[0]
                context = {'product':product,
                        'storeManager':storeManager,
                        'search_query': search_query,
                        'order': order,
                        'carts': carts,}
                return render(request, 'professional_service_admin/product-list.html',context)
            else:
                context = {'product':product,
                            'storeManager':storeManager,
                            'search_query': search_query,
                            'orders': orders,
                            'carts': carts,}
                return render(request, 'professional_service_admin/product-list.html',context)
                

@login_required(login_url='admin_login')
def generate_random_product_ID():
    N = 4
    string_var = ""
    string_var = ''.join(random.choices(string.digits, k=N))
    string_var = "#M-" + string_var
    return string_var

@csrf_exempt
@login_required(login_url='admin_login')
def add_product(request):
    if request.user.is_storeManager:
     user = StoreManager.objects.get(user=request.user)
     
    if request.method == 'POST':
       product = Product()
       
       if 'featured_image' in request.FILES:
           featured_image = request.FILES['featured_image']
       else:
           featured_image = "products/default.png"
       
       name = request.POST.get('name')
       ServiceRequest_reqiuired = request.POST.get('requirement_type')     
       weight = request.POST.get('weight') 
       quantity = request.POST.get('quantity')
       product_category = request.POST.get('category_type')
       product_type = request.POST.get('product_type')
       description = request.POST.get('description')
       price = request.POST.get('price')
       
       product.name = name
       product.ServiceRequest_reqiuired = ServiceRequest_reqiuired
       product.weight = weight
       productquantity = quantity
       product.product_category = product_category
       product.product_type = product_type
       product.description = description
       product.price = price
       product.featured_image = featured_image
       product.stock_quantity = 80
       #product.product_id = generate_random_product_ID()
       
       product.save()
       
       return redirect('product-list')
   
    return render(request, 'professional_service_admin/add-product.html',{'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def edit_product(request, pk):
    if request.user.is_storeManager:
        user = StoreManager.objects.get(user=request.user)
        
        product = Product.objects.get(serial_number=pk)
        old_product_image = product.featured_image
        
        if request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = old_product_image
                name = request.POST.get('name')
                ServiceRequest_reqiuired = request.POST.get('requirement_type')     
                weight = request.POST.get('weight') 
                quantity = request.POST.get('quantity')
                product_category = request.POST.get('category_type')
                product_type = request.POST.get('product_type')
                description = request.POST.get('description')
                price = request.POST.get('price')
                
                product.name = name
                product.ServiceRequest_reqiuired = ServiceRequest_reqiuired
                product.weight = weight
                product.quantity = quantity
                product.product_category = product_category
                product.product_type = product_type
                product.description = description
                product.price = price
                product.featured_image = featured_image
                product.stock_quantity = 80
                #product.product_id = generate_random_product_ID()
            
                product.save()
            
                return redirect('product-list')
   
    return render(request, 'professional_service_admin/edit-product.html',{'product': product,'admin': user})


@csrf_exempt
@login_required(login_url='admin_login')
def delete_product(request, pk):
    if request.user.is_storeManager:
        user = StoreManager.objects.get(user=request.user)
        product = Product.objects.get(serial_number=pk)
        product.delete()
        return redirect('product-list')

@csrf_exempt
@login_required(login_url='admin_login')
def add_technical_specialist(request):
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        
        form = TechnicalSpecialistCreationForm()
     
        if request.method == 'POST':
            form = TechnicalSpecialistCreationForm(request.POST)
            if form.is_valid():
                # form.save(), commit=False --> don't save to database yet (we have a chance to modify object)
                user = form.save(commit=False)
                user.is_technicalSpecialist = True
                user.save()

                messages.success(request, 'Clinical Laboratory Technician account was created!')

                # After user is created, we can log them in
                #login(request, user)
                return redirect('technical-specialist-list')
            else:
                messages.error(request, 'An error has occurred during registration')
    
    context = {'form': form, 'admin': user}
    return render(request, 'professional_service_admin/add-technical-specialist.html', context)  

@csrf_exempt
@login_required(login_url='admin_login')
def view_technical_specialist(request):
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        technical_specialists = Clinical_Laboratory_Technician.objects.all()
        
    return render(request, 'professional_service_admin/technical-specialist-list.html', {'technical_specialists': technical_specialists, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def view_storeManager(request):
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        pharmcists = StoreManager.objects.all()
        
    return render(request, 'professional_service_admin/storeManager-list.html', {'storeManager': pharmcists, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def edit_technical_specialist(request, pk):
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        technical_specialist = Clinical_Laboratory_Technician.objects.get(technician_id=pk)
        
        if request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = "technician/user-default.png"
                
            name = request.POST.get('name')
            email = request.POST.get('email')     
            phone_number = request.POST.get('phone_number')
            age = request.POST.get('age')  
    
            technical_specialist.name = name
            technical_specialist.email = email
            technical_specialist.phone_number = phone_number
            technical_specialist.age = age
            technical_specialist.featured_image = featured_image
    
            technical_specialist.save()
            
            messages.success(request, 'Clinical Laboratory Technician account updated!')
            return redirect('technical-specialist-list')
        
    return render(request, 'professional_service_admin/edit-technical-specialist.html', {'technical_specialist': technical_specialist, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def edit_storeManager(request, pk):
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        storeManager = StoreManager.objects.get(storeManager_id=pk)
        
        if request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = "technician/user-default.png"
                
            name = request.POST.get('name')
            email = request.POST.get('email')     
            phone_number = request.POST.get('phone_number')
            age = request.POST.get('age')  
    
            storeManager.name = name
            storeManager.email = email
            storeManager.phone_number = phone_number
            storeManager.age = age
            storeManager.featured_image = featured_image
    
            storeManager.save()
            messages.success(request, 'StoreManager updated!')
            return redirect('storeManager-list')
        
    return render(request, 'professional_service_admin/edit-storeManager.html', {'storeManager': storeManager, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def profession_image_list(request,pk):
    professions = ServiceDepartment.objects.filter(professional_service_id=pk)
    #departments = ServiceDepartment.objects.all()
    context = {'professions': professions}
    return render(request, 'professional_service_admin/profession-image-list.html',context)

@csrf_exempt
@login_required(login_url='admin_login')
def register_professional_list(request):
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        professionals = Professional_Information.objects.filter(register_status='Accepted')
    return render(request, 'professional_service_admin/register-professional-list.html', {'professionals': professionals, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def pending_professional_list(request):
    if request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
    professionals = Professional_Information.objects.filter(register_status='Pending')
    return render(request, 'professional_service_admin/Pending-professional-list.html', {'all': professionals, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def admin_professional_profile(request,pk):
    professional = Professional_Information.objects.get(professional_id=pk)
    admin = Admin_Information.objects.get(user=request.user)
    experience= Experience.objects.filter(professional_id=pk).order_by('-from_year','-to_year')
    education = Education.objects.filter(professional_id=pk).order_by('-year_of_completion')
    
    context = {'professional': professional, 'admin': admin, 'experiences': experience, 'educations': education}
    return render(request, 'professional_service_admin/professional-profile.html',context)


@csrf_exempt
@login_required(login_url='admin_login')
def accept_professional(request,pk):
    professional = Professional_Information.objects.get(professional_id=pk)
    professional.register_status = 'Accepted'
    professional.save()
    
    experience= Experience.objects.filter(professional_id=pk)
    education = Education.objects.filter(professional_id=pk)
    
    # Mailtrap
    professional_name = professional.name
    professional_email = professional.email
    professional_profession = professional.profession_name.ServiceDepartment_name

    professional_specialization = professional.specialization.specialization_name

    subject = "Acceptance of Professional Registration"

    values = {
            "professional_name":professional_name,
            "professional_email":professional_email,
            "professional_profession":professional_profession,

            "professional_specialization":professional_specialization,
        }

    html_message = render_to_string('professional_service_admin/accept-professional-mail.html', {'values': values})
    plain_message = strip_tags(html_message)

    try:
        send_mail(subject, plain_message, 'professional_service_admin@gmail.com',  [professional_email], html_message=html_message, fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found')

    messages.success(request, 'Professional Accepted!')
    return redirect('register-professional-list')


@csrf_exempt
@login_required(login_url='admin_login')
def reject_professional(request,pk):
    professional = Professional_Information.objects.get(professional_id=pk)
    professional.register_status = 'Rejected'
    professional.save()
    
    # Mailtrap
    professional_name = professional.name
    professional_email = professional.email
    professional_profession = professional.profession_name.ServiceDepartment_name
    professional_professional_service = professional.service_name.name
    professional_specialization = professional.specialization.specialization_name

    subject = "Rejection of Professional Registration"

    values = {
            "professional_name":professional_name,
            "professional_email":professional_email,
            "professional_profession":professional_profession,
            "professional_professional_service":professional_professional_service,
            "professional_specialization":professional_specialization,
        }

    html_message = render_to_string('professional_service_admin/reject-professional-mail.html', {'values': values})
    plain_message = strip_tags(html_message)

    try:
        send_mail(subject, plain_message, 'professional_service_admin@gmail.com',  [professional_email], html_message=html_message, fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found')
    
    messages.success(request, 'Professional Rejected!')
    return redirect('register-professional-list')

@csrf_exempt
@login_required(login_url='admin_login')
def delete_profession(request,pk):
    if request.user.is_authenticated:
        if request.user.is_professional_service_admin:
            profession = ServiceDepartment.objects.get(ServiceDepartment_id=pk)
            profession.delete()
            messages.success(request, 'Department Deleted!')
            return redirect('professional_service-list')

@login_required(login_url='admin_login')
@csrf_exempt
def edit_profession(request,pk):
    if request.user.is_authenticated:
        if request.user.is_professional_service_admin:
            # old_featured_image = profession.featured_image
            profession = ServiceDepartment.objects.get(ServiceDepartment_id=pk)
            old_featured_image = profession.featured_image

            if request.method == 'POST':
                if 'featured_image' in request.FILES:
                    featured_image = request.FILES['featured_image']
                else:
                    featured_image = old_featured_image

                profession_name = request.POST.get('profession_name')
                profession.ServiceDepartment_name = profession_name
                profession.featured_image = featured_image
                profession.save()
                messages.success(request, 'Department Updated!')
                return redirect('professional_service-list')
                
            context = {'profession': profession}
            return render(request, 'professional_service_admin/edit-professional_service.html',context)

@csrf_exempt
@login_required(login_url='admin_login')
def technicalSpecialist_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_technicalSpecialist:
            
            technical_specialists = Clinical_Laboratory_Technician.objects.get(user=request.user)
            professional = Professional_Information.objects.all()
            context = {'professional': professional,'technical_specialists':technical_specialists}
            return render(request, 'professional_service_admin/technicalSpecialist-dashboard.html',context)

@csrf_exempt
@login_required(login_url='admin-login')
def myclient_list(request):
    if request.user.is_authenticated:
        if request.user.is_technicalSpecialist:
            technical_specialists = Clinical_Laboratory_Technician.objects.get(user=request.user)
            #report= Report.objects.all()
            client = Client.objects.all()
            context = {'client': client,'technical_specialists':technical_specialists}
            return render(request, 'professional_service_admin/myclient-list.html',context)

@csrf_exempt
@login_required(login_url='admin-login')
def serviceRequest_list(request,pk):
    if request.user.is_authenticated:
        if request.user.is_technicalSpecialist:
            technical_specialists = Clinical_Laboratory_Technician.objects.get(user=request.user)
            client = Client.objects.get(client_id=pk)
            serviceRequest = ServiceRequest.objects.filter(client=client)
            context = {'serviceRequest': serviceRequest,'technical_specialists':technical_specialists,'client':client}
            return render(request, 'professional_service_admin/serviceRequest-list.html',context)

@csrf_exempt
@login_required(login_url='admin-login')
def add_test(request):
    if request.user.is_technicalSpecialist:
        technical_specialists = Clinical_Laboratory_Technician.objects.get(user=request.user)

    if request.method == 'POST':
        tests=Test_Information()
        test_name = request.POST['test_name']
        test_price = request.POST['test_price']
        tests.test_name = test_name
        tests.test_price = test_price

        tests.save()

        return redirect('test-list')
        
    context = {'technical_specialists': technical_specialists}
    return render(request, 'professional_service_admin/add-test.html', context)

@csrf_exempt
@login_required(login_url='admin-login')
def test_list(request):
    if request.user.is_technicalSpecialist:
        technical_specialists = Clinical_Laboratory_Technician.objects.get(user=request.user)
        test = Test_Information.objects.all()
        context = {'test':test,'technical_specialists':technical_specialists}
    return render(request, 'professional_service_admin/test-list.html',context)


@csrf_exempt
@login_required(login_url='admin-login')
def delete_test(request,pk):
    if request.user.is_authenticated:
        if request.user.is_technicalSpecialist:
            test = Test_Information.objects.get(test_id=pk)
            test.delete()
            return redirect('test-list')

@csrf_exempt
def storeManager_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_storeManager:
            storeManager = StoreManager.objects.get(user=request.user)
            total_storeManager_count = StoreManager.objects.annotate(count=Count('storeManager_id'))
            total_product_count = Product.objects.annotate(count=Count('serial_number'))
            total_order_count = ServiceOrder.objects.annotate(count=Count('orderitems'))
            total_cart_count = Cart.objects.annotate(count=Count('item'))

            product = Product.objects.all()
            
            context = {'storeManager':storeManager, 'product':product,
                       'total_storeManager_count':total_storeManager_count, 
                       'total_product_count':total_product_count, 
                       'total_order_count':total_order_count,
                       'total_cart_count':total_cart_count}
            return render(request, 'professional_service_admin/storeManager-dashboard.html',context)

@csrf_exempt
def report_history(request):
    if request.user.is_authenticated:
        if request.user.is_technicalSpecialist:

            technical_specialists = Clinical_Laboratory_Technician.objects.get(user=request.user)
            report = Report.objects.all()
            context = {'report':report,'technical_specialists':technical_specialists}
            return render(request, 'professional_service_admin/report-list.html',context)

