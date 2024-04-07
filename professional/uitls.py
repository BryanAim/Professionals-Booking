from django.db.models import Q
from .models import Client, User, ServiceProvider
from professional.models import Professional_Information, Appointment
from service_provider_admin.models import ServiceDepartment, specialization, service


def searchClients(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    #skills = Skill.objects.filter(name__icontains=search_query)
    
    client = Client.objects.filter(
        Q(client_id__icontains=search_query))
    
    return client, search_query
