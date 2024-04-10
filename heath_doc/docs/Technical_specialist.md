# Technical Specialist

## What does a laboratory Worker do

A lab tech is a person who performs the practical hands-on work in laboratories. Laboratory technicians have a wide range of responsibilities that might vary depending on their particular laboratory setting. These day-to-day tasks may include:

- Collecting samples of blood and other substances

- Performing lab tests on samples and analyzing results

- Ensuring quality control of samples

- Adhering to a laboratory’s standards and policies

- Preparing samples and processing them as needed

- Logging test results into clients’ medical records

## Report Creation By Technical Specialist

```python
def create_report(request, pk):
    if request.user.is_technicalSpecialist:
        technical_specialists = Technical_Specialist.objects.get(user=request.user)
        serviceRequest =ServiceRequest.objects.get(serviceRequest_id=pk)
        client = Client.objects.get(client_id=serviceRequest.client_id)
        professional = Professional_Information.objects.get(professional_id=serviceRequest.professional_id)
        tests = ServiceRequest_test.objects.filter(serviceRequest=serviceRequest).filter(test_info_pay_status='Paid')


        if request.method == 'POST':
            report = Report(professional=professional, client=client)

            specimen_type = request.POST.getlist('specimen_type')
            collection_date  = request.POST.getlist('collection_date')
            receiving_date = request.POST.getlist('receiving_date')
            test_name = request.POST.getlist('test_name')
            result = request.POST.getlist('result')
            unit = request.POST.getlist('unit')
            referred_value = request.POST.getlist('referred_value')
            delivery_date = request.POST.get('delivery_date')
            other_information= request.POST.get('other_information')
            report.delivery_date = delivery_date
            report.other_information = other_information

            report.save()

            for i in range(len(specimen_type)):
                specimens = Specimen(report=report)
                specimens.specimen_type = specimen_type[i]
                specimens.collection_date = collection_date[i]
                specimens.receiving_date = receiving_date[i]
                specimens.save()

            for i in range(len(test_name)):
                tests = Test(report=report)
                tests.test_name=test_name[i]
                tests.result=result[i]
                tests.unit=unit[i]
                tests.referred_value=referred_value[i]
                tests.save()


            return redirect('myclient-list')

        context = {'serviceRequest':serviceRequest,'technical_specialists':technical_specialists,'tests':tests}
        return render(request, 'service_provider_admin/create-report.html',context)
```

## Technical Specialist Dashboard

This is the dasboard of the lab worker.

![title](technical_specialist /Screenshot (237).png)

## Pending Report List

![title](technical_specialist /Screenshot (238).png)

## Create Test Form

![title](technical_specialist /Screenshot (240).png)

## Viewing Test List

![title](technical_specialist /Screenshot (239).png)
