from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    customerNumber = models.CharField(primary_key=True, max_length=128, unique=True)
    customerFirstName = models.CharField(max_length=64, default="")
    customerLastName = models.CharField(max_length=64, default="")
    contactFirstName = models.CharField(max_length=64)
    contactLastName = models.CharField(max_length=64)
    phone = models.CharField(max_length=15)
    addressOne = models.CharField(max_length=128)
    addressTwo = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=64)
    postalCode = models.CharField(max_length=8)
    country = models.CharField(max_length=64)
    creditLimit = models.IntegerField(default=100)
    signUpDate = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.customerNumber

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customerNumber = models.ForeignKey(Customer)
    def __str__(self):
        return self.user.username

class ProductLine(models.Model):
    productLine = models.CharField(primary_key=True, max_length=128, unique=True)
    textDescription = models.TextField()
    htmlDescription = models.TextField()
    image = models.ImageField()
    def __str__(self):
        return self.ProductLine

class Product(models.Model):
    productCode = models.CharField(primary_key=True, max_length=128, unique=True)
    productName = models.CharField(max_length=128)
    productLine = models.ForeignKey(ProductLine)
    productScale = models.CharField(max_length=128)
    productDescription = models.CharField(max_length=128)
    quantityInStock = models.IntegerField()
    buyPrice = models.IntegerField()
    MSRP = models.IntegerField()
    def __str__(self):
        return self.productCode

class Order(models.Model):
    orderNumber = models.CharField(primary_key=True, max_length=128, unique=True)
    orderDate = models.DateField()
    requiredDate = models.DateField()
    shippedDate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=32)
    comments = models.CharField(max_length=256)
    customerNumber = models.ForeignKey(Customer)
    def __str__(self):
        return self.orderNumber

class OrderDetail(models.Model):
    orderNumber = models.ForeignKey(Order)
    productCode = models.ForeignKey(Product)
    quantityOrdered = models.IntegerField()
    priceEach = models.IntegerField()
    orderLineNumber = models.IntegerField()
    def __str__(self):
        return self.orderNumber

class Payment(models.Model):
    customerNumber = models.ForeignKey(Customer)
    checkNumber = models.CharField(primary_key=True, max_length=128, unique=True)
    paymentDate = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.customerNumber

class Office(models.Model):
    officeCode = models.IntegerField(primary_key=True, unique=True)
    phone = models.CharField(max_length=15)
    addressOne = models.CharField(max_length=128)
    addressTwo = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=64)
    postalCode = models.CharField(max_length=8)
    country = models.CharField(max_length=64)
    territory = models.CharField(max_length=64)

    def __str__(self):
        return str(self.officeCode)

class Employee(models.Model):
    employeeNumber = models.CharField(primary_key=True, max_length=128, unique=True)
    lastName = models.CharField(max_length=128)
    firstName = models.CharField(max_length=128)
    extension = models.IntegerField()
    email = models.EmailField()
    officeCode = models.ForeignKey(Office)
    reportsTo = models.ForeignKey("self")
    jobTitle = models.CharField(max_length=128)
    def __str__(self):
        return self.employeeNumber
