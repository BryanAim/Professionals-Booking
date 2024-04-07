# Welcome to Professional

We have developed a convenient professional/client interface to bring you a service that allows you to have a medical consultation.

## The main duties of a Professional :

- Accept or appointments from clients.
- View client profile after accepting appointments.
- Can register himself to a specific service_provider.
- Search clients.
- Create prescription.
- Sending mail to the client about appointment confirmation.
- Chat with client.
- Professional Profile settings.

## Accepting Appointments of clients

```python
def accept_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    appointment.appointment_status = 'confirmed'
    appointment.save()

    client_email = appointment.client.email
    client_name = appointment.client.name
    client_username = appointment.client.username
    client_serial_number = appointment.client.serial_number
    professional_name = appointment.professional.name

    appointment_serial_number = appointment.serial_number
    appointment_date = appointment.date
    appointment_time = appointment.time
    appointment_status = appointment.appointment_status

    subject = "Appointment Acceptance Email"

    values = {
            "email":client_email,
            "name":client_name,
            "username":client_username,
            "serial_number":client_serial_number,
            "professional_name":professional_name,
            "appointment_serial_num":appointment_serial_number,
            "appointment_date":appointment_date,
            "appointment_time":appointment_time,
            "appointment_status":appointment_status,
    }

    html_message = render_to_string('appointment_accept_mail.html', {'values': values})
    plain_message = strip_tags(html_message)

    try:
        send_mail(subject, plain_message, 'service_provider_admin@gmail.com',  [client_email], html_message=html_message, fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found')

    messages.success(request, 'Appointment Accepted')

    return redirect('professional-dashboard')
```

## Professional Dashboard

![title](professional/Screenshot (218).png)

## Professional Profile

![title](professional/Screenshot (219).png)

## Search ServiceProvider

![title](professional/Screenshot (220).png)

## Search Clients

```python
def client_search(request, pk):
    if request.user.is_authenticated and request.user.is_professional:
        professional = Professional_Information.objects.get(professional_id=pk)
        id = int(request.GET['search_query'])
        client = Client.objects.get(client_id=id)
        prescription = Prescription.objects.filter(professional=professional).filter(client=client)
        context = {'client': client, 'professional': professional, 'prescription': prescription}
        return render(request, 'client-profile.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'professional-login.html')

```

## Create Prescription

```python
def create_prescription(request,pk):
        if request.user.is_professional:
            professional = Professional_Information.objects.get(user=request.user)
            client = Client.objects.get(client_id=pk)
            create_date = datetime.date.today()


            if request.method == 'POST':
                prescription = Prescription(professional=professional, client=client)

                test_name= request.POST.getlist('test_name')
                test_description = request.POST.getlist('description')
                medicine_name = request.POST.getlist('medicine_name')
                medicine_quantity = request.POST.getlist('quantity')
                medecine_frequency = request.POST.getlist('frequency')
                medicine_duration = request.POST.getlist('duration')
                medicine_relation_with_meal = request.POST.getlist('relation_with_meal')
                medicine_instruction = request.POST.getlist('instruction')
                extra_information = request.POST.get('extra_information')
                test_info_id = request.POST.getlist('id')


                prescription.extra_information = extra_information
                prescription.create_date = create_date

                prescription.save()

                for i in range(len(medicine_name)):
                    medicine = Prescription_medicine(prescription=prescription)
                    medicine.medicine_name = medicine_name[i]
                    medicine.quantity = medicine_quantity[i]
                    medicine.frequency = medecine_frequency[i]
                    medicine.duration = medicine_duration[i]
                    medicine.instruction = medicine_instruction[i]
                    medicine.relation_with_meal = medicine_relation_with_meal[i]
                    medicine.save()

                for i in range(len(test_name)):
                    tests = Prescription_test(prescription=prescription)
                    tests.test_name = test_name[i]
                    tests.test_description = test_description[i]
                    tests.test_info_id = test_info_id[i]
                    test_info = Test_Information.objects.get(test_id=test_info_id[i])
                    tests.test_info_price = test_info.test_price

                    tests.save()

                messages.success(request, 'Prescription Created')
                return redirect('client-profile', pk=client.client_id)

        context = {'professional': professional,'client': client}
        return render(request, 'create-prescription.html',context)
```

## Profile Settings

![title](professional/Screenshot (223).png)
