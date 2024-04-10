# Welcome to StoreManager

## The main duties of a storeManager includes:

- `Administrative tasks such as add products information.`
- `Edit medicine information.`
- `Delete medicine information.`
- `Search medicine.`
- `View Product information.`

## Add products into database

```python
def add_medicine(request):
    if request.user.is_storeManager:
     user = StoreManager.objects.get(user=request.user)

    if request.method == 'POST':
       medicine = Product()

       if 'featured_image' in request.FILES:
           featured_image = request.FILES['featured_image']
       else:
           featured_image = "products/default.png"

       name = request.POST.get('name')
       ServiceRequest_reqiuired = request.POST.get('requirement_type')
       weight = request.POST.get('weight')
       quantity = request.POST.get('quantity')
       medicine_category = request.POST.get('category_type')
       medicine_type = request.POST.get('medicine_type')
       description = request.POST.get('description')
       price = request.POST.get('price')

       medicine.name = name
       medicine.Prescription_reqiuired = Prescription_reqiuired
       medicine.weight = weight
       medicine.quantity = quantity
       medicine.medicine_category = medicine_category
       medicine.medicine_type = medicine_type
       medicine.description = description
       medicine.price = price
       medicine.featured_image = featured_image
       medicine.stock_quantity = 80
       #medicine.medicine_id = generate_random_medicine_ID()

       medicine.save()

       return redirect('medicine-list')

    return render(request, 'professional_service_admin/add-medicine.html',{'admin': user})
```

## Product Table

![title](storeManager /Screenshot (244).png)
