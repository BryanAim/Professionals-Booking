from io import BytesIO
from urllib import response
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from professional.models import Prescription
from professional.models import  Prescription,Prescription_product,Prescription_test
from service_provider.models import Client
from datetime import datetime


def render_to_pdf(template_src, context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pres_pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pres_pdf.err:
        return HttpResponse(result.getvalue(),content_type="aplication/pres_pdf")
    return None




def prescription_pdf(request,pk):
 if request.user.is_client:
    client = Client.objects.get(user=request.user)
    prescription = Prescription.objects.get(prescription_id=pk)
    prescription_product = Prescription_product.objects.filter(prescription=prescription)
    prescription_test = Prescription_test.objects.filter(prescription=prescription)
    # current_date = datetime.date.today()
    context={'client':client,'prescriptions':prescription,'prescription_test':prescription_test,'prescription_product':prescription_product}
    pres_pdf=render_to_pdf('prescription_pdf.html', context)
    if pres_pdf:
        response=HttpResponse(pres_pdf, content_type='application/pres_pdf')
        content="inline; filename=prescription.pdf"
        response['Content-Disposition']= content
        return response
    return HttpResponse("Not Found")
