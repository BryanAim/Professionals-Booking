from django.db.models import Q
from .models import Product


def searchProducts(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
            
    products = Product.objects.filter(Q(name__icontains=search_query))
    
    return products, search_query
