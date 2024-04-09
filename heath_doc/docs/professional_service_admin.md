# Welcome To ProfessionalService Admin

ProfessionalService Admin is a cruical User for our project.

## ProfessionalService Admin Task

- Accept / Reject Professional
- Add and View Technicalspecialist
- Add and View StoreManager
- Add,Edit and View ProfessionalService
- Update ProfessionalService Information

# Accept/Reject professional

```python
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

    html_message = render_to_string('professional_service_admin/accept-professional-mail.html', {'values': values})
    plain_message = strip_tags(html_message)

    try:
        send_mail(subject, plain_message, 'professional_service_admin@gmail.com',  [professional_email], html_message=html_message, fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found')

    messages.success(request, 'Professional Accepted!')
    return redirect('register-professional-list')

def reject_professional(request,pk):
    professional = Professional_Information.objects.get(professional_id=pk)
    professional.register_status = 'Rejected'
    professional.save()

    # Mailtrap
    professional_name = professional.name
    professional_email = professional.email
    professional_department = professional.department_name.ServiceDepartment_name
    professional_professional_service = professional.service_name.name
    professional_specialization = professional.specialization.specialization_name

    subject = "Rejection of Professional Registration"

    values = {
            "professional_name":professional_name,
            "professional_email":professional_email,
            "professional_department":professional_department,
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
```

![title](admins/professional-list.png)

# Add and View Technicalspecialist

```python
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
```

![title](admins/add labratory.png)
![title](admins/view labratory.png)

# Add and View StoreManager

```python
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
```

![title](admins/add storeManager.png)
![title](admins/view storeManager.png)

# Add,Edit and View ProfessionalService

```python
def add_professional_service(request):
    if  request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)

        if request.method == 'POST':
            professional_service = ProfessionalService()

            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = "departments/default.png"

            service_name = request.POST.get('service_name')
            address = request.POST.get('address')
            description = request.POST.get('description')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            profession = request.POST.get('type')
            specialization_name = request.POST.getlist('specialization')
            department_name = request.POST.getlist('department')
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

            for i in range(len(department_name)):
                departments = ServiceDepartment(professional_service=professional_service)
                # print(department_name[i])
                departments.ServiceDepartment_name = department_name[i]
                departments.save()

            for i in range(len(specialization_name)):
                specializations = specialization(professional_service=professional_service)
                specializations.specialization_name=specialization_name[i]
                specializations.save()

            for i in range(len(service_name)):
                services = service(professional_service=professional_service)
                services.service_name = service_name[i]
                services.save()

            messages.success(request, 'ProfessionalService Added')
            return redirect('professional_service-list')

        context = { 'admin': user}
        return render(request, 'professional_service_admin/add-professional_service.html',context)
```

![title](admins/add professional_service info.png)

# Edit ProfessionalService Information

```python
def edit_professional_service(request, pk):
    if  request.user.is_professional_service_admin:
        user = Admin_Information.objects.get(user=request.user)
        professional_service = ProfessionalService.objects.get(professional_service_id=pk)
        old_featured_image = professional_service.featured_image

        if request.method == 'GET':
            specializations = specialization.objects.filter(professional_service=professional_service)
            services = service.objects.filter(professional_service=professional_service)
            departments = ServiceDepartment.objects.filter(professional_service=professional_service)
            context = {'professional_service': professional_service, 'specializations': specializations, 'services': services,'departments':departments, 'admin': user}
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
            department_name = request.POST.getlist('department')
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

            for i in range(len(department_name)):
                departments = ServiceDepartment(professional_service=professional_service)
                departments.ServiceDepartment_name = department_name[i]
                departments.save()

            messages.success(request, 'ProfessionalService Updated')
            return redirect('professional_service-list')

```

![title](admins/edit professional_service information.png)
