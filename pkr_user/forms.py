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
        exclude = ('creditLimit', 'signUpDate', 'customerNumber')

class ProductForm(forms.ModelForm):
    class Meta():
        model = models.Product
        exclude = ()
