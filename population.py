import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PKR.settings')

import django
django.setup()

#Fake POP
import random
import pkr_user.models as models
from faker import Faker

fakegen = Faker()
productLine = ['Vegetables', 'Liquids', 'Condiments', 'Processed', 'Meats']

def add_productLine():
    t = models.ProductLine.objects.get_or_create(productLine=random.choice(productLine))[0]
    t.save()
    return t

if __name__ == '__main__':
    print("Populating product lines!")
    for n in range(10):
        add_productLine()
    print("Populating product lines complete!!")
