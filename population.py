import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PKR.settings')

import django
django.setup()

#Fake POP
import random
import pkr_user.models as models
from faker import Faker
import uuid
from datetime import date, timedelta

fakegen = Faker()
productLine = ['Vegetables', 'Liquids', 'Condiments', 'Processed', 'Meats']
productName = ['Ice Cream' , 'Iceberg Lettuce', 'Strawberries', 'Glutinous Rice']
def add_productLine():
    t = models.ProductLine.objects.get_or_create(productLine=random.choice(productLine))[0]
    t.save()
    return t

def createProducts():
    t = add_productLine()
    productCode = fakegen.ean13()
    fakeproductName =random.choice(productName)
    quantityInStock = fakegen.pyint()
    price = fakegen.pyfloat(left_digits=2, right_digits=2, positive=True)
    MSRP = fakegen.pyfloat(left_digits=2, right_digits=2, positive=True)
    customer = models.Customer.objects.order_by('?').first()
    new = models.Product.objects.get_or_create(productCode=productCode,
                                             productName=fakeproductName,
                                             productLine = t,
                                             quantityInStock=quantityInStock,
                                             buyPrice=price,
                                             MSRP=MSRP,
                                             customerNumber=customer)[0]
    new.save()
    createStocks(customer, new)

def createStocks(customer, product):
    productCode = models.Product.objects.values_list('productCode', 'customerNumber').order_by('?').first()
    newproductCode = models.Product.objects.get(customerNumber=customer, productCode=product)
    for day in range(21):
        fake_date = date.today() - timedelta(days=day)
        quantityInStock = fakegen.pyint()
        new = models.Stock.objects.get_or_create(productCode=newproductCode, dateRecord=fake_date, quantity=quantityInStock, customerNumber=customer)[0]
        new.save()

if __name__ == '__main__':
    # p = models.Product.objects.values_list('productCode', 'customerNumber').order_by('?').first()
    # c = models.Customer.objects.get(customerNumber=p[1])
    # stock = models.Stock.objects.get(productCode=p, customerNumber=c)
    # print("Populating product lines!")
    for n in range(50):
        createProducts()
    #createStocks()
    #print("Populating product lines complete!!")
