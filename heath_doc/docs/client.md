# Welcome to Client Dashboard

## The main services a client avail:

- `Visit multiple professional_service, get emargency information of a professional_service, and also gets professional information.`
- `Search departmant`
- `Book professional appointment`
- `Search Professional `
- `View ServiceRequest`
- `Book tests and pay online`
- `View Report history`
- `Profile edit`
- `Get mail for appointment and payment`
- `Product Shop, Search Product, and buy Product`

## View professional_service Information

```python
def professional_service_profile(request, pk):

    if request.user.is_authenticated:

        if request.user.is_client:
            client = Client.objects.get(user=request.user)
            professionals = Professional_Information.objects.all()
            professional_services = ProfessionalService.objects.get(professional_service_id=pk)

            departments = ServiceDepartment.objects.filter(professional_service=professional_services)
            specializations = specialization.objects.filter(professional_service=professional_services)
            services = service.objects.filter(professional_service=professional_services)

            context = {'client': client, 'professionals': professionals, 'professional_services': professional_services, 'departments': departments, 'specializations': specializations, 'services': services}
            return render(request, 'professional_service-profile.html', context)

        elif request.user.is_professional:

            professional = Professional_Information.objects.get(user=request.user)
            professional_services = ProfessionalService.objects.get(professional_service_id=pk)

            departments = ServiceDepartment.objects.filter(professional_service=professional_services)
            specializations = specialization.objects.filter(professional_service=professional_services)
            services = service.objects.filter(professional_service=professional_services)

            context = {'professional': professional, 'professional_services': professional_services, 'departments': departments, 'specializations': specializations, 'services': services}
            return render(request, 'professional_service-profile.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')
```

## View Multiple ProfessionalService Information

![title](client/Screenshot (254).png)
![title](client/Screenshot (253).png)

## View professional_service Professional Information

```python
def professional_service_professional_list(request, pk):
    if request.user.is_authenticated and request.user.is_client:
        # client = Client.objects.get(user_id=pk)
        client = Client.objects.get(user=request.user)
        departments = ServiceDepartment.objects.get(ServiceDepartment_id=pk)
        professionals = Professional_Information.objects.filter(department_name=departments)

        professionals, search_query = searchDepartmentProfessionals(request, pk)

        context = {'client': client, 'department': departments, 'professionals': professionals, 'search_query': search_query, 'pk_id': pk}
        return render(request, 'professional_service-professional-list.html', context)

    elif request.user.is_authenticated and request.user.is_professional:
        # client = Client.objects.get(user_id=pk)

        professional = Professional_Information.objects.get(user=request.user)
        departments = ServiceDepartment.objects.get(ServiceDepartment_id=pk)

        professionals = Professional_Information.objects.filter(department_name=departments)
        professionals, search_query = searchDepartmentProfessionals(request, pk)

        context = {'professional':professional, 'department': departments, 'professionals': professionals, 'search_query': search_query, 'pk_id': pk}
        return render(request, 'professional_service-professional-list.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')
```

## Professional Information Page

![title](client/Screenshot (213).png)

## View professional_service Professional Information

```python
 def booking(request, pk):
    client = request.user.client
    professional = Professional_Information.objects.get(professional_id=pk)

    if request.method == 'POST':
        appointment = Appointment(client=client, professional=professional)
        date = request.POST['appoint_date']
        time = request.POST['appoint_time']
        appointment_type = request.POST['appointment_type']
        message = request.POST['message']


        transformed_date = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
        transformed_date = str(transformed_date)

        appointment.date = transformed_date
        appointment.time = time
        appointment.appointment_status = 'pending'
        appointment.serial_number = generate_random_string()
        appointment.appointment_type = appointment_type
        appointment.message = message
        appointment.save()

        if message:
            # Mailtrap
            client_email = appointment.client.email
            client_name = appointment.client.name
            client_username = appointment.client.username
            client_phone_number = appointment.client.phone_number
            professional_name = appointment.professional.name

            subject = "Appointment Request"

            values = {
                    "email":client_email,
                    "name":client_name,
                    "username":client_username,
                    "phone_number":client_phone_number,
                    "professional_name":professional_name,
                    "message":message,
                }

            html_message = render_to_string('appointment-request-mail.html', {'values': values})
            plain_message = strip_tags(html_message)

            try:
                send_mail(subject, plain_message, 'professional_service_admin@gmail.com',  [client_email], html_message=html_message, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found')


        messages.success(request, 'Appointment Booked')
        return redirect('client-dashboard')

    context = {'client': client, 'professional': professional}
    return render(request, 'booking.html', context)
```

## Book Professional Appointment Page

![title](client/Screenshot (256).png)

## View ServiceRequestInformation

```python
 def serviceRequest_view(request,pk):
      if request.user.is_client:
        client = Client.objects.get(user=request.user)
        serviceRequest = ServiceRequest.objects.filter(serviceRequest_id=pk)
        serviceRequest_product = ServiceRequest_medicine.objects.filter(serviceRequest__in=serviceRequest)
        serviceRequest_test = ServiceRequest_test.objects.filter(serviceRequest__in=serviceRequest)

        context = {'client':client,'serviceRequest':serviceRequest,'serviceRequest_test':serviceRequest_test,'serviceRequest_product':serviceRequest_product}
        return render(request, 'serviceRequest-view.html',context)
      else:
         redirect('logout')
```

## ServiceRequestPage

![title](client/Screenshot (212).png)

## View Test Payment Method

```python
def test_cart(request, pk):
    if request.user.is_authenticated and request.user.is_client:
        # serviceRequest = ServiceRequest.objects.filter(serviceRequest_id=pk)

        serviceRequest = ServiceRequest.objects.filter(serviceRequest_id=pk)

        client = Client.objects.get(user=request.user)
        serviceRequest_test = ServiceRequest_test.objects.all()
        test_carts = testCart.objects.filter(user=request.user, purchased=False)
        test_orders = testOrder.objects.filter(user=request.user, ordered=False)

        if test_carts.exists() and test_orders.exists():
            test_order = test_orders[0]

            context = {'test_carts': test_carts,'test_order': test_order, 'client': client, 'serviceRequest_test':serviceRequest_test, 'serviceRequest_id':pk}
            return render(request, 'test-cart.html', context)
        else:
            # messages.warning(request, "You don't have any test in your cart!")
            context = {'client': client,'serviceRequest_test':serviceRequest_test}
            return render(request, 'serviceRequest-view.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'client-login.html')
```

## Payment Page

![title](payment/Screenshot (249).png)

## View Report History

```python
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
```

## Report View

![title](payment/Screenshot (249).png)

## View Product Shop

```python
  def store_shop(request):
    if request.user.is_authenticated and request.user.is_client:

        client = Client.objects.get(user=request.user)
        products = Product.objects.all()
        orders = ServiceOrder.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)

        products, search_query = searchProducts(request)

        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'client': client, 'products': products,'carts': carts,'order': order, 'orders': orders, 'search_query': search_query}
            return render(request, 'Store/shop.html', context)
        else:
            context = {'client': client, 'products': products,'carts': carts,'orders': orders, 'search_query': search_query}
            return render(request, 'Store/shop.html', context)

    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')
```

## Product Shop Page

![title](store/Screenshot (246).png)

## Product Shop Cart

```python
def cart_view(request):
    if request.user.is_authenticated and request.user.is_client:

        client = Client.objects.get(user=request.user)
        products = Product.objects.all()

        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = ServiceOrder.objects.filter(user=request.user, ordered=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'carts': carts,'order': order}
            return render(request, 'Store/cart.html', context)
        else:
            messages.warning(request, "You don't have any item in your cart!")
            context = {'client': client,'products': products}
            return render(request, 'store/shop.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'client-login.html')

```

## Product Shop cart page

![title](store/Screenshot (247).png)
