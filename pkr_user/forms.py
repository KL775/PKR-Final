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
        # customerNumber = models.CharField(primary_key=True, max_length=128, unique=True)
        # customerFirstName = models.CharField(max_length=64, default="")
        # customerLastName = models.CharField(max_length=64, default="")
        # contactFirstName = models.CharField(max_length=64)
        # contactLastName = models.CharField(max_length=64)
        # phone = models.CharField(max_length=15)
        # addressOne = models.CharField(max_length=128)
        # addressTwo = models.CharField(max_length=128, blank=True, null=True)
        # city = models.CharField(max_length=64)
        # postalCode = models.CharField(max_length=8)
        # country = models.CharField(max_length=64)
        exclude = ('creditLimit', 'signUpDate', 'customerNumber')

class ProductForm(forms.ModelForm):
    class Meta():
        model = models.Product
        exclude = ()
