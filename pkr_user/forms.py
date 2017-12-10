from django import forms
from django.contrib.auth.models import User
import pkr_user.models as models


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password')

class CustomerForm(forms.ModelForm):
    class Meta():
        model = models.Customer
        labels = {
            "customerFirstName" : "First Name",
            "customerLastName" : "Last Name",
            "contactFirstName" : "Contact First Name",
            "contactLastName" : "Contact Last Name",
            "postalCode" : "Postal Code",
            "addressOne" : "Address Line One",
            "addressTwo" : "Address Line Two",
        }
        exclude = ('creditLimit', 'signUpDate', 'customerNumber')

class ProductForm(forms.ModelForm):
    class Meta():
        model = models.Product
        labels = {
            "productCode" : "Product Code",
            "productName" : "Product Name",
            "productLine" : "Product Line",
            "quantityInStock" : "Quantity",
            "buyPrice" : "Buy Price",
            "MSRP" : "Retail Price",
        }
        exclude = ('productScale', 'productDescription', 'customerNumber')
