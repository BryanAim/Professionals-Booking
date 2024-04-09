from io import BytesIO
from urllib import response
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from professional.models import ServiceRequest
from professional.models import  ServiceRequest,Perscription_product,Perscription_test
from professional_service.models import Client
from datetime import datetime


def render_to_pdf(template_src, context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="aplication/pdf")
    return None




def serviceRequest_pdf(request,pk):
 if request.user.is_client:
    client = Client.objects.get(user=request.user)
    serviceRequest = ServiceRequest.objects.get(serviceRequest_id=pk)
    perscription_product = Perscription_product.objects.filter(serviceRequest=serviceRequest)
    perscription_test = Perscription_test.objects.filter(serviceRequest=serviceRequest)
    current_date = datetime.date.today()
    context={'client':client,'current_date' : current_date,'serviceRequest':serviceRequest,'perscription_test':perscription_test,'perscription_product':perscription_product}
    pdf=render_to_pdf('serviceRequest_pdf.html', context)
    if pdf:
        response=HttpResponse(pdf, content_type='application/pdf')
        content="inline; filename=report.pdf"
        # response['Content-Disposition']= content
        return response
    return HttpResponse("Not Found")
