from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProfessionalServiceSerializer
from professional_service.models import Professional_Service_Information, Client, User 
from professional.models import Professional_Information

@api_view(['GET'])
def getRoutes(request):
    # Specify which urls (routes) to accept
    
    routes = [
        {'GET': '/api/professional_service/'},
        {'GET': '/api/professional_service/id'},

        # to test built-in authentication - JSON web tokens have an expiration date
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)

# @permission_classes([IsAuthenticated]) # set up a restricted route

@api_view(['GET'])
def getProfessionalServices(request):
    professional_services = Professional_Service_Information.objects.all() # query the database (get python object)
    serializer = ProfessionalServiceSerializer(professional_services, many=True) # convert python object to JSON object
    # many=True because we are serializing a list of objects
    return Response(serializer.data)


@api_view(['GET'])
def getProfessionalServiceProfile(request, pk):
    professional_services = Professional_Service_Information.objects.get(professional_service_id=pk)
    serializer = ProfessionalServiceSerializer(professional_services, many=False) # many=False for a single object
    return Response(serializer.data)
