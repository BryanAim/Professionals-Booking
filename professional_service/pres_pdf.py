from io import BytesIO
from urllib import response
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from professional.models import ServiceRequest
from professional.models import  ServiceRequest,ServiceRequest_product,ServiceRequest_test
from professional_service.models import Client
from datetime import datetime


def render_to_pdf(template_src, context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pres_pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pres_pdf.err:
        return HttpResponse(result.getvalue(),content_type="aplication/pres_pdf")
    return None




def serviceRequest_pdf(request,pk):
 if request.user.is_client:
    client = Client.objects.get(user=request.user)
    serviceRequest = ServiceRequest.objects.get(serviceRequest_id=pk)
    serviceRequest_product = ServiceRequest_product.objects.filter(serviceRequest=serviceRequest)
    serviceRequest_test = ServiceRequest_test.objects.filter(serviceRequest=serviceRequest)
    # current_date = datetime.date.today()
    context={'client':client,'serviceRequests':serviceRequest,'serviceRequest_test':serviceRequest_test,'serviceRequest_product':serviceRequest_product}
    pres_pdf=render_to_pdf('serviceRequest_pdf.html', context)
    if pres_pdf:
        response=HttpResponse(pres_pdf, content_type='application/pres_pdf')
        content="inline; filename=serviceRequest.pdf"
        response['Content-Disposition']= content
        return response
    return HttpResponse("Not Found")
