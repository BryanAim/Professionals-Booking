from django.db.models import Q
from .models import Client, User, Professional_Service_Information
from professional.models import Professional_Information, Appointment
from professional_service_admin.models import ServiceDepartment, specialization, service
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProfessionals(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    #skills = Skill.objects.filter(name__icontains=search_query)
    
    professionals = Professional_Information.objects.filter(register_status='Accepted').distinct().filter(
        Q(name__icontains=search_query) |
        Q(service_name__name__icontains=search_query) |  
        Q(profession__icontains=search_query))
    
    return professionals, search_query



def searchProfessionalServices(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    
    professional_services = Professional_Service_Information.objects.distinct().filter(Q(name__icontains=search_query))
    
    return professional_services, search_query


def paginateProfessionalServices(request, professional_services, results):

    page = request.GET.get('page')
    paginator = Paginator(professional_services, results)

    try:
        professional_services = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        professional_services = paginator.page(page)
    except EmptyPage:
        # display last page if page is out of range
        page = paginator.num_pages
        professional_services = paginator.page(page)
        
    
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
    return custom_range, professional_services


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
        
    professions = ServiceDepartment.objects.get(ServiceDepartment_id=pk)
    
    professionals = Professional_Information.objects.filter(profession_name=professions).filter(
        Q(name__icontains=search_query))
    
    # professionals = Professional_Information.objects.filter(department_name=departments).filter(
    #     Q(name__icontains=search_query) |
    #     Q(specialization_name__name__icontains=search_query))
    
    return professionals, search_query



# products = Products.objects.filter(price__range=[10, 100])
