from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ServiceProviderSerializer
from service_provider.models import ServiceProvider, Client, User 
from professional.models import Professional_Information

@api_view(['GET'])
def getRoutes(request):
    # Specify which urls (routes) to accept
    
    routes = [
        {'GET': '/api/service_provider/'},
        {'GET': '/api/service_provider/id'},

        # to test built-in authentication - JSON web tokens have an expiration date
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)

# @permission_classes([IsAuthenticated]) # set up a restricted route

@api_view(['GET'])
def getServiceProviders(request):
    service_providers = ServiceProvider.objects.all() # query the database (get python object)
    serializer = ServiceProviderSerializer(service_providers, many=True) # convert python object to JSON object
    # many=True because we are serializing a list of objects
    return Response(serializer.data)


@api_view(['GET'])
def getServiceProviderProfile(request, pk):
    service_providers = ServiceProvider.objects.get(service_provider_id=pk)
    serializer = ServiceProviderSerializer(service_providers, many=False) # many=False for a single object
    return Response(serializer.data)
