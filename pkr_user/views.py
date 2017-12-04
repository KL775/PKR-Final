from django.shortcuts import render
import pkr_user.forms as forms
from pkr_user.models import UserProfile
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import uuid

def home(request):
    return render(request, 'pkr_user/home.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        customer_form = forms.CustomerForm(data = request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            customer = customer_form.save()
            customer.signUpDate = timezone.now()
            customer.customerNumber = uuid.uuid4()
            customer.creditLimit = 100
            customer.save()
            user = user_form.save()
            user.set_password(user.password)
            user.first_name = customer.customerFirstName
            user.last_name = customer.customerLastName
            user.save()
            user_customer = UserProfile(customerNumber=customer, user=user)
            user_customer.save()
            registered = True
        else:
            print(user_form.errors, customer_form.errors)
    else:
        user_form = forms.UserForm()
        customer_form = forms.CustomerForm()
    return render(request, 'pkr_user/register.html',
                { 'user_form' : user_form,
                  'customer_form' : customer_form,
                  'registered' : registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'pkr_user/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
