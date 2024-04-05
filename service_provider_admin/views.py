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
from service_provider.models import ServiceProvider, User, Client
from django.db.models import Q
from pharmacy.models import Product, Pharmacist
from professional.models import Professional_Information, Prescription, Prescription_test, Report, Appointment, Experience , Education,Specimen,Test
from pharmacy.models import ServiceOrder, Cart
from sslcommerz.models import Payment
from .forms import AdminUserCreationForm, LabWorkerCreationForm, EditHospitalForm, EditEmergencyForm,AdminForm , PharmacistCreationForm 

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
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
        total_client_count = Client.objects.annotate(count=Count('client_id'))
        total_professional_count = Professional_Information.objects.annotate(count=Count('professional_id'))
        total_pharmacist_count = Pharmacist.objects.annotate(count=Count('pharmacist_id'))
        total_hospital_count = ServiceProvider.objects.annotate(count=Count('hospital_id'))
        total_labworker_count = Clinical_Laboratory_Technician.objects.annotate(count=Count('technician_id'))
        pending_appointment = Appointment.objects.filter(appointment_status='pending').count()
        professionals = Professional_Information.objects.all()
        clients = Client.objects.all()
        service_providers = ServiceProvider.objects.all()
        lab_workers = Clinical_Laboratory_Technician.objects.all()
        pharmacists = Pharmacist.objects.all()
        
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

        context = {'admin': user,'total_client_count': total_client_count,'total_professional_count':total_professional_count,'pending_appointment':pending_appointment,'professionals':professionals,'clients':clients,'service_providers':service_providers,'lab_workers':lab_workers,'total_pharmacist_count':total_pharmacist_count,'total_hospital_count':total_hospital_count,'total_labworker_count':total_labworker_count,'sat_count': sat_count, 'sun_count': sun_count, 'mon_count': mon_count, 'tues_count': tues_count, 'wed_count': wed_count, 'thurs_count': thurs_count, 'fri_count': fri_count, 'sat': sat, 'sun': sun, 'mon': mon, 'tues': tues, 'wed': wed, 'thurs': thurs, 'fri': fri, 'pharmacists': pharmacists}
        return render(request, 'hospital_admin/admin-dashboard.html', context)
    elif request.user.is_labworker:
        # messages.error(request, 'You are not authorized to access this page')
        return redirect('labworker-dashboard')
    # return render(request, 'hospital_admin/admin-dashboard.html', context)

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
        return render(request, 'hospital_admin/login.html')
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
            if user.is_hospital_admin:
                messages.success(request, 'User logged in')
                return redirect('admin-dashboard')
            elif user.is_labworker:
                messages.success(request, 'User logged in')
                return redirect('labworker-dashboard')
            elif user.is_pharmacist:
                messages.success(request, 'User logged in')
                return redirect('pharmacist-dashboard')
            else:
                return redirect('admin-logout')
        else:
            messages.error(request, 'Invalid username or password')
        

    return render(request, 'hospital_admin/login.html')


@csrf_exempt
def admin_register(request):
    page = 'hospital_admin/register'
    form = AdminUserCreationForm()

    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            # commit=False --> don't save to database yet (we have a chance to modify object)
            user = form.save(commit=False)
            user.is_hospital_admin = True
            user.save()

            messages.success(request, 'User account was created!')
            
            # After user is created, we can log them in
            #login(request, user)
            return redirect('admin_login')

        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'hospital_admin/register.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def admin_forgot_password(request):
    return render(request, 'hospital_admin/forgot-password.html')

@csrf_exempt
@login_required(login_url='admin_login')
def invoice(request):
    return render(request, 'hospital_admin/invoice.html')

@csrf_exempt
@login_required(login_url='admin_login')
def invoice_report(request):
    return render(request, 'hospital_admin/invoice-report.html')

@login_required(login_url='admin_login')
def lock_screen(request):
    return render(request, 'hospital_admin/lock-screen.html')

@csrf_exempt
@login_required(login_url='admin_login')
def client_list(request):
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
    clients = Client.objects.all()
    return render(request, 'hospital_admin/client-list.html', {'all': clients, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def specialitites(request):
    return render(request, 'hospital_admin/specialities.html')

@csrf_exempt
@login_required(login_url='admin_login')
def appointment_list(request):
    return render(request, 'hospital_admin/appointment-list.html')

@login_required(login_url='admin_login')
def transactions_list(request):
    return render(request, 'hospital_admin/transactions-list.html')

@csrf_exempt
@login_required(login_url='admin_login')
def emergency_details(request):
    user = Admin_Information.objects.get(user=request.user)
    service_providers = ServiceProvider.objects.all()
    context = { 'admin': user, 'all': service_providers}
    return render(request, 'hospital_admin/emergency.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def hospital_list(request):
    user = Admin_Information.objects.get(user=request.user)
    service_providers = ServiceProvider.objects.all()
    context = { 'admin': user, 'service_providers': service_providers}
    return render(request, 'hospital_admin/hospital-list.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def appointment_list(request):
    return render(request, 'hospital_admin/appointment-list.html')

@csrf_exempt
@login_required(login_url='admin_login')
def hospital_profile(request):
    return render(request, 'hospital-profile.html')

@csrf_exempt
@login_required(login_url='admin_login')
def hospital_admin_profile(request, pk):

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
    return render(request, 'hospital_admin/hospital-admin-profile.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def add_hospital(request):
    if  request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)

        if request.method == 'POST':
            hospital = ServiceProvider()
            
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = "departments/default.png"
            
            hospital_name = request.POST.get('hospital_name')
            address = request.POST.get('address')
            description = request.POST.get('description')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number') 
            hospital_type = request.POST.get('type')
            specialization_name = request.POST.getlist('specialization')
            department_name = request.POST.getlist('department')
            service_name = request.POST.getlist('service')
            
        
            hospital.name = hospital_name
            hospital.description = description
            hospital.address = address
            hospital.email = email
            hospital.phone_number =phone_number
            hospital.featured_image=featured_image 
            hospital.hospital_type=hospital_type
            
            # print(department_name[0])
         
            hospital.save()
            
            for i in range(len(department_name)):
                departments = ServiceDepartment(service_provider=hospital)
                # print(department_name[i])
                departments.ServiceDepartment_name = department_name[i]
                departments.save()
                
            for i in range(len(specialization_name)):
                specializations = specialization(service_provider=hospital)
                specializations.specialization_name=specialization_name[i]
                specializations.save()
                
            for i in range(len(service_name)):
                services = service(service_provider=hospital)
                services.service_name = service_name[i]
                services.save()
            
            messages.success(request, 'Hospital Added')
            return redirect('hospital-list')

        context = { 'admin': user}
        return render(request, 'hospital_admin/add-hospital.html',context)


# def edit_hospital(request, pk):
#     hospital = ServiceProvider.objects.get(hospital_id=pk)
#     return render(request, 'hospital_admin/edit-hospital.html')

@csrf_exempt
@login_required(login_url='admin_login')
def edit_hospital(request, pk):
    if  request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
        hospital = ServiceProvider.objects.get(hospital_id=pk)
        old_featured_image = hospital.featured_image

        if request.method == 'GET':
            specializations = specialization.objects.filter(service_provider=hospital)
            services = service.objects.filter(service_provider=hospital)
            departments = ServiceDepartment.objects.filter(service_provider=hospital)
            context = {'hospital': hospital, 'specializations': specializations, 'services': services,'departments':departments, 'admin': user}
            return render(request, 'hospital_admin/edit-hospital.html',context)

        elif request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = old_featured_image
                               
            hospital_name = request.POST.get('hospital_name')
            address = request.POST.get('address')
            description = request.POST.get('description')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number') 
            hospital_type = request.POST.get('type')
            
            specialization_name = request.POST.getlist('specialization')
            department_name = request.POST.getlist('department')
            service_name = request.POST.getlist('service')

            hospital.name = hospital_name
            hospital.description = description
            hospital.address = address
            hospital.email = email
            hospital.phone_number =phone_number
            hospital.featured_image =featured_image 
            hospital.hospital_type =hospital_type
            
            # specializations.specialization_name=specialization_name
            # services.service_name = service_name
            # departments.ServiceDepartment_name = department_name 

            hospital.save()

            # Specialization
            for i in range(len(specialization_name)):
                specializations = specialization(service_provider=hospital)
                specializations.specialization_name = specialization_name[i]
                specializations.save()

            # Experience
            for i in range(len(service_name)):
                services = service(service_provider=hospital)
                services.service_name = service_name[i]
                services.save()
                
            for i in range(len(department_name)):
                departments = ServiceDepartment(service_provider=hospital)
                departments.ServiceDepartment_name = department_name[i]
                departments.save()

            messages.success(request, 'Hospital Updated')
            return redirect('hospital-list')

@csrf_exempt
@login_required(login_url='admin_login')
def delete_specialization(request, pk, pk2):
    specializations = specialization.objects.get(specialization_id=pk)
    specializations.delete()
    messages.success(request, 'Delete Specialization')
    return redirect('edit-hospital', pk2)

@csrf_exempt
@login_required(login_url='admin_login')
def delete_service(request, pk, pk2):
    services = service.objects.get(service_id=pk)
    services.delete()
    messages.success(request, 'Delete Service')
    return redirect('edit-hospital', pk2)

@csrf_exempt
@login_required(login_url='admin_login')
def edit_emergency_information(request, pk):

    hospital = ServiceProvider.objects.get(hospital_id=pk)
    form = EditEmergencyForm(instance=hospital)  

    if request.method == 'POST':
        form = EditEmergencyForm(request.POST, request.FILES,
                           instance=hospital)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Emergency information added')
            return redirect('emergency')
        else:
            form = EditEmergencyForm()

    context = {'hospital': hospital, 'form': form}
    return render(request, 'hospital_admin/edit-emergency-information.html', context)

@csrf_exempt
@login_required(login_url='admin_login')
def delete_hospital(request, pk):
	hospital = ServiceProvider.objects.get(hospital_id=pk)
	hospital.delete()
	return redirect('hospital-list')


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
    if  request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)

    client = Client.objects.get(client_id=pk)

    if request.method == 'POST':
        invoice = Payment(client=client)
        
        consulation_fee = request.POST['consulation_fee']
        report_fee = request.POST['report_fee']
        #total_ammount = request.POST['currency_amount']
        invoice.currency_amount = int(consulation_fee) + int(report_fee)
        invoice.consulation_fee = consulation_fee
        invoice.report_fee = report_fee
        invoice.invoice_number = generate_random_invoice()
        invoice.name = client
        invoice.status = 'Pending'
    
        invoice.save()
        return redirect('client-list')

    context = {'client': client,'admin': user}
    return render(request, 'hospital_admin/create-invoice.html', context)


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
    if request.user.is_labworker:
        lab_workers = Clinical_Laboratory_Technician.objects.get(user=request.user)
        prescription =Prescription.objects.get(prescription_id=pk)
        client = Client.objects.get(client_id=prescription.client_id)
        professional = Professional_Information.objects.get(professional_id=prescription.professional_id)
        tests = Prescription_test.objects.filter(prescription=prescription).filter(test_info_pay_status='Paid')
        

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

            html_message = render_to_string('hospital_admin/report-mail-delivery.html', {'values': values})
            plain_message = strip_tags(html_message)

            try:
                send_mail(subject, plain_message, 'hospital_admin@gmail.com',  [client_email], html_message=html_message, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found') 

            return redirect('myclientlist')

        context = {'prescription':prescription,'lab_workers':lab_workers,'tests':tests}
        return render(request, 'hospital_admin/create-report.html',context)

@csrf_exempt
@login_required(login_url='admin_login')
def add_pharmacist(request):
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
        form = PharmacistCreationForm()
     
        if request.method == 'POST':
            form = PharmacistCreationForm(request.POST)
            if form.is_valid():
                # form.save(), commit=False --> don't save to database yet (we have a chance to modify object)
                user = form.save(commit=False)
                user.is_pharmacist = True
                user.save()

                messages.success(request, 'Pharmacist account was created!')

                # After user is created, we can log them in
                #login(request, user)
                return redirect('pharmacist-list')
            else:
                messages.error(request, 'An error has occurred during registration')
    
    context = {'form': form, 'admin': user}
    return render(request, 'hospital_admin/add-pharmacist.html', context)
  
@csrf_exempt
@login_required(login_url='admin_login')
def product_list(request):
    if request.user.is_authenticated:
        if request.user.is_pharmacist:
            pharmacist = Pharmacist.objects.get(user=request.user)
            product = Product.objects.all()
            orders = ServiceOrder.objects.filter(user=request.user, ordered=False)
            carts = Cart.objects.filter(user=request.user, purchased=False)
            
            product, search_query = searchProduct(request)
            
            if carts.exists() and orders.exists():
                order = orders[0]
                context = {'product':product,
                        'pharmacist':pharmacist,
                        'search_query': search_query,
                        'order': order,
                        'carts': carts,}
                return render(request, 'hospital_admin/product-list.html',context)
            else:
                context = {'product':product,
                            'pharmacist':pharmacist,
                            'search_query': search_query,
                            'orders': orders,
                            'carts': carts,}
                return render(request, 'hospital_admin/product-list.html',context)
                

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
    if request.user.is_pharmacist:
     user = Pharmacist.objects.get(user=request.user)
     
    if request.method == 'POST':
       product = Product()
       
       if 'featured_image' in request.FILES:
           featured_image = request.FILES['featured_image']
       else:
           featured_image = "products/default.png"
       
       name = request.POST.get('name')
       Prescription_reqiuired = request.POST.get('requirement_type')     
       weight = request.POST.get('weight') 
       quantity = request.POST.get('quantity')
       product_category = request.POST.get('category_type')
       product_type = request.POST.get('product_type')
       description = request.POST.get('description')
       price = request.POST.get('price')
       
       product.name = name
       product.Prescription_reqiuired = Prescription_reqiuired
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
   
    return render(request, 'hospital_admin/add-product.html',{'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def edit_product(request, pk):
    if request.user.is_pharmacist:
        user = Pharmacist.objects.get(user=request.user)
        
        product = Product.objects.get(serial_number=pk)
        old_product_image = product.featured_image
        
        if request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = old_product_image
                name = request.POST.get('name')
                Prescription_reqiuired = request.POST.get('requirement_type')     
                weight = request.POST.get('weight') 
                quantity = request.POST.get('quantity')
                product_category = request.POST.get('category_type')
                product_type = request.POST.get('product_type')
                description = request.POST.get('description')
                price = request.POST.get('price')
                
                product.name = name
                product.Prescription_reqiuired = Prescription_reqiuired
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
   
    return render(request, 'hospital_admin/edit-product.html',{'product': product,'admin': user})


@csrf_exempt
@login_required(login_url='admin_login')
def delete_product(request, pk):
    if request.user.is_pharmacist:
        user = Pharmacist.objects.get(user=request.user)
        product = Product.objects.get(serial_number=pk)
        product.delete()
        return redirect('product-list')

@csrf_exempt
@login_required(login_url='admin_login')
def add_lab_worker(request):
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
        
        form = LabWorkerCreationForm()
     
        if request.method == 'POST':
            form = LabWorkerCreationForm(request.POST)
            if form.is_valid():
                # form.save(), commit=False --> don't save to database yet (we have a chance to modify object)
                user = form.save(commit=False)
                user.is_labworker = True
                user.save()

                messages.success(request, 'Clinical Laboratory Technician account was created!')

                # After user is created, we can log them in
                #login(request, user)
                return redirect('lab-worker-list')
            else:
                messages.error(request, 'An error has occurred during registration')
    
    context = {'form': form, 'admin': user}
    return render(request, 'hospital_admin/add-lab-worker.html', context)  

@csrf_exempt
@login_required(login_url='admin_login')
def view_lab_worker(request):
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
        lab_workers = Clinical_Laboratory_Technician.objects.all()
        
    return render(request, 'hospital_admin/lab-worker-list.html', {'lab_workers': lab_workers, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def view_pharmacist(request):
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
        pharmcists = Pharmacist.objects.all()
        
    return render(request, 'hospital_admin/pharmacist-list.html', {'pharmacist': pharmcists, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def edit_lab_worker(request, pk):
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
        lab_worker = Clinical_Laboratory_Technician.objects.get(technician_id=pk)
        
        if request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = "technician/user-default.png"
                
            name = request.POST.get('name')
            email = request.POST.get('email')     
            phone_number = request.POST.get('phone_number')
            age = request.POST.get('age')  
    
            lab_worker.name = name
            lab_worker.email = email
            lab_worker.phone_number = phone_number
            lab_worker.age = age
            lab_worker.featured_image = featured_image
    
            lab_worker.save()
            
            messages.success(request, 'Clinical Laboratory Technician account updated!')
            return redirect('lab-worker-list')
        
    return render(request, 'hospital_admin/edit-lab-worker.html', {'lab_worker': lab_worker, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def edit_pharmacist(request, pk):
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
        pharmacist = Pharmacist.objects.get(pharmacist_id=pk)
        
        if request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = "technician/user-default.png"
                
            name = request.POST.get('name')
            email = request.POST.get('email')     
            phone_number = request.POST.get('phone_number')
            age = request.POST.get('age')  
    
            pharmacist.name = name
            pharmacist.email = email
            pharmacist.phone_number = phone_number
            pharmacist.age = age
            pharmacist.featured_image = featured_image
    
            pharmacist.save()
            messages.success(request, 'Pharmacist updated!')
            return redirect('pharmacist-list')
        
    return render(request, 'hospital_admin/edit-pharmacist.html', {'pharmacist': pharmacist, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def department_image_list(request,pk):
    departments = ServiceDepartment.objects.filter(hospital_id=pk)
    #departments = ServiceDepartment.objects.all()
    context = {'departments': departments}
    return render(request, 'hospital_admin/department-image-list.html',context)

@csrf_exempt
@login_required(login_url='admin_login')
def register_professional_list(request):
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
        professionals = Professional_Information.objects.filter(register_status='Accepted')
    return render(request, 'hospital_admin/register-professional-list.html', {'professionals': professionals, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def pending_professional_list(request):
    if request.user.is_hospital_admin:
        user = Admin_Information.objects.get(user=request.user)
    professionals = Professional_Information.objects.filter(register_status='Pending')
    return render(request, 'hospital_admin/Pending-professional-list.html', {'all': professionals, 'admin': user})

@csrf_exempt
@login_required(login_url='admin_login')
def admin_professional_profile(request,pk):
    professional = Professional_Information.objects.get(professional_id=pk)
    admin = Admin_Information.objects.get(user=request.user)
    experience= Experience.objects.filter(professional_id=pk).order_by('-from_year','-to_year')
    education = Education.objects.filter(professional_id=pk).order_by('-year_of_completion')
    
    context = {'professional': professional, 'admin': admin, 'experiences': experience, 'educations': education}
    return render(request, 'hospital_admin/professional-profile.html',context)


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
    professional_department = professional.department_name.ServiceDepartment_name

    professional_specialization = professional.specialization.specialization_name

    subject = "Acceptance of Professional Registration"

    values = {
            "professional_name":professional_name,
            "professional_email":professional_email,
            "professional_department":professional_department,

            "professional_specialization":professional_specialization,
        }

    html_message = render_to_string('hospital_admin/accept-professional-mail.html', {'values': values})
    plain_message = strip_tags(html_message)

    try:
        send_mail(subject, plain_message, 'hospital_admin@gmail.com',  [professional_email], html_message=html_message, fail_silently=False)
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
    professional_department = professional.department_name.ServiceDepartment_name
    professional_hospital = professional.hospital_name.name
    professional_specialization = professional.specialization.specialization_name

    subject = "Rejection of Professional Registration"

    values = {
            "professional_name":professional_name,
            "professional_email":professional_email,
            "professional_department":professional_department,
            "professional_hospital":professional_hospital,
            "professional_specialization":professional_specialization,
        }

    html_message = render_to_string('hospital_admin/reject-professional-mail.html', {'values': values})
    plain_message = strip_tags(html_message)

    try:
        send_mail(subject, plain_message, 'hospital_admin@gmail.com',  [professional_email], html_message=html_message, fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found')
    
    messages.success(request, 'Professional Rejected!')
    return redirect('register-professional-list')

@csrf_exempt
@login_required(login_url='admin_login')
def delete_department(request,pk):
    if request.user.is_authenticated:
        if request.user.is_hospital_admin:
            department = ServiceDepartment.objects.get(ServiceDepartment_id=pk)
            department.delete()
            messages.success(request, 'Department Deleted!')
            return redirect('hospital-list')

@login_required(login_url='admin_login')
@csrf_exempt
def edit_department(request,pk):
    if request.user.is_authenticated:
        if request.user.is_hospital_admin:
            # old_featured_image = department.featured_image
            department = ServiceDepartment.objects.get(ServiceDepartment_id=pk)
            old_featured_image = department.featured_image

            if request.method == 'POST':
                if 'featured_image' in request.FILES:
                    featured_image = request.FILES['featured_image']
                else:
                    featured_image = old_featured_image

                department_name = request.POST.get('department_name')
                department.ServiceDepartment_name = department_name
                department.featured_image = featured_image
                department.save()
                messages.success(request, 'Department Updated!')
                return redirect('hospital-list')
                
            context = {'department': department}
            return render(request, 'hospital_admin/edit-hospital.html',context)

@csrf_exempt
@login_required(login_url='admin_login')
def labworker_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_labworker:
            
            lab_workers = Clinical_Laboratory_Technician.objects.get(user=request.user)
            professional = Professional_Information.objects.all()
            context = {'professional': professional,'lab_workers':lab_workers}
            return render(request, 'hospital_admin/labworker-dashboard.html',context)

@csrf_exempt
@login_required(login_url='admin-login')
def myclient_list(request):
    if request.user.is_authenticated:
        if request.user.is_labworker:
            lab_workers = Clinical_Laboratory_Technician.objects.get(user=request.user)
            #report= Report.objects.all()
            client = Client.objects.all()
            context = {'client': client,'lab_workers':lab_workers}
            return render(request, 'hospital_admin/myclient-list.html',context)

@csrf_exempt
@login_required(login_url='admin-login')
def prescription_list(request,pk):
    if request.user.is_authenticated:
        if request.user.is_labworker:
            lab_workers = Clinical_Laboratory_Technician.objects.get(user=request.user)
            client = Client.objects.get(client_id=pk)
            prescription = Prescription.objects.filter(client=client)
            context = {'prescription': prescription,'lab_workers':lab_workers,'client':client}
            return render(request, 'hospital_admin/prescription-list.html',context)

@csrf_exempt
@login_required(login_url='admin-login')
def add_test(request):
    if request.user.is_labworker:
        lab_workers = Clinical_Laboratory_Technician.objects.get(user=request.user)

    if request.method == 'POST':
        tests=Test_Information()
        test_name = request.POST['test_name']
        test_price = request.POST['test_price']
        tests.test_name = test_name
        tests.test_price = test_price

        tests.save()

        return redirect('test-list')
        
    context = {'lab_workers': lab_workers}
    return render(request, 'hospital_admin/add-test.html', context)

@csrf_exempt
@login_required(login_url='admin-login')
def test_list(request):
    if request.user.is_labworker:
        lab_workers = Clinical_Laboratory_Technician.objects.get(user=request.user)
        test = Test_Information.objects.all()
        context = {'test':test,'lab_workers':lab_workers}
    return render(request, 'hospital_admin/test-list.html',context)


@csrf_exempt
@login_required(login_url='admin-login')
def delete_test(request,pk):
    if request.user.is_authenticated:
        if request.user.is_labworker:
            test = Test_Information.objects.get(test_id=pk)
            test.delete()
            return redirect('test-list')

@csrf_exempt
def pharmacist_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_pharmacist:
            pharmacist = Pharmacist.objects.get(user=request.user)
            total_pharmacist_count = Pharmacist.objects.annotate(count=Count('pharmacist_id'))
            total_product_count = Product.objects.annotate(count=Count('serial_number'))
            total_order_count = ServiceOrder.objects.annotate(count=Count('orderitems'))
            total_cart_count = Cart.objects.annotate(count=Count('item'))

            product = Product.objects.all()
            
            context = {'pharmacist':pharmacist, 'product':product,
                       'total_pharmacist_count':total_pharmacist_count, 
                       'total_product_count':total_product_count, 
                       'total_order_count':total_order_count,
                       'total_cart_count':total_cart_count}
            return render(request, 'hospital_admin/pharmacist-dashboard.html',context)

@csrf_exempt
def report_history(request):
    if request.user.is_authenticated:
        if request.user.is_labworker:

            lab_workers = Clinical_Laboratory_Technician.objects.get(user=request.user)
            report = Report.objects.all()
            context = {'report':report,'lab_workers':lab_workers}
            return render(request, 'hospital_admin/report-list.html',context)

