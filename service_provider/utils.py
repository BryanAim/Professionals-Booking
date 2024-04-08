from django.db.models import Q
from .models import Client, User, Service_Provider_Information
from professional.models import Professional_Information, Appointment
from service_provider_admin.models import ServiceDepartment, specialization, service
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProfessionals(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    #skills = Skill.objects.filter(name__icontains=search_query)
    
    professionals = Professional_Information.objects.filter(register_status='Accepted').distinct().filter(
        Q(name__icontains=search_query) |
        Q(service_name__name__icontains=search_query) |  
        Q(service_type__icontains=search_query))
    
    return professionals, search_query



def searchServiceProviders(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    
    service_providers = Service_Provider_Information.objects.distinct().filter(Q(name__icontains=search_query))
    
    return service_providers, search_query


def paginateServiceProviders(request, service_providers, results):

    page = request.GET.get('page')
    paginator = Paginator(service_providers, results)

    try:
        service_providers = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        service_providers = paginator.page(page)
    except EmptyPage:
        # display last page if page is out of range
        page = paginator.num_pages
        service_providers = paginator.page(page)
        
    
    # if there are many pages, we will see some at a time in the pagination bar (range window)
    # leftIndex(left button) = current page no. - 4 
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        # if leftIndex is less than 1, we will start from 1
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    # return custom_range, projects, paginator
    return custom_range, service_providers


# def searchDepartmentProfessionals(request, pk):
    
#     search_query = ''
    
#     if request.GET.get('search_query'):
#         search_query = request.GET.get('search_query')
        
    
#     departments = hospital_department.object.filter(hospital_department_id=pk).filter(
#         Q(professional__name__icontains=search_query) |  
#         Q(professional__department__icontains=search_query))
    
#     return departments, search_query

def searchDepartmentProfessionals(request, pk):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    service_types = ServiceDepartment.objects.get(ServiceDepartment_id=pk)
    
    professionals = Professional_Information.objects.filter(service_type_name=service_types).filter(
        Q(name__icontains=search_query))
    
    # professionals = Professional_Information.objects.filter(department_name=departments).filter(
    #     Q(name__icontains=search_query) |
    #     Q(specialization_name__name__icontains=search_query))
    
    return professionals, search_query



# products = Products.objects.filter(price__range=[10, 100])
