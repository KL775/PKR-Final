from django.shortcuts import render
import pkr_user.forms as forms
import pkr_user.models as models
from pkr_user.models import UserProfile
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
import uuid
import csv

def home(request):
    return render(request, 'pkr_user/home.html')

@login_required
def dashboard(request):
    product_form = forms.ProductForm
    stock_form = forms.StockForm
    error = messages.get_messages(request)
    return render(request, 'pkr_user/dashboard.html', {"product_form" : product_form, "stock_form" : stock_form, "error" : error})

@login_required
def add_product(request):
    current_user = request.user
    product_form = forms.ProductForm(data=request.POST)
    stock_form = forms.StockForm(data=request.POST)
    profile = models.UserProfile.objects.values_list('customerNumber').get(user=current_user)
    curr_customer = models.Customer.objects.get(customerNumber=profile[0])
    if product_form.is_valid() and stock_form.is_valid():
        product = product_form.save()
        product.customerNumber = curr_customer
        product.save()
        stock = models.Stock.objects.get_or_create(productCode=product, dateRecord=timezone.now(), quantity=0, customerNumber=curr_customer)[0]
        print(stock_form.cleaned_data['quantity'])
        stock.quantity = stock_form.cleaned_data['quantity']
        stock.save()
    else:
        print(product_form.errors)
    return HttpResponseRedirect(reverse('dashboard'))

def update_stock(request):
    print("Updating Stock!")
    current_user = request.user
    profile = models.UserProfile.objects.values_list('customerNumber').get(user=current_user)
    curr_customer = models.Customer.objects.get(customerNumber=profile[0])
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        product_id = models.Product.objects.get(productCode=request.POST.get('id'))
        product_name = models.Product.objects.values_list('productName').get(productCode=request.POST.get('id'))
        try:
            exist_stock = models.Stock.objects.get(customerNumber=curr_customer, productCode=product_id, dateRecord=timezone.now())
            print(product_name)
            messages.add_message(request, messages.INFO, 'You cannot update ' + product_name[0] + ' again today.')
            return HttpResponseRedirect(reverse('dashboard'))
        except models.Stock.DoesNotExist:
            new = models.Stock.objects.get_or_create(productCode=product_id, dateRecord=timezone.now(), quantity=quantity, customerNumber=curr_customer)[0]
            new.save()
    print("End Path!")
    return HttpResponseRedirect(reverse('dashboard'))

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

@login_required
def items(request): # GET endpoint should work in dashboard.html
    #query db to get table of (itemID, itemName) tuples
    current_user = request.user
    if request.user.is_authenticated():
        profile = models.UserProfile.objects.values_list('customerNumber').get(user=current_user)
        curr_customer = models.Customer.objects.get(customerNumber=profile[0])
        items = models.Product.objects.values_list('productCode', 'productName').filter(customerNumber=curr_customer).distinct('productName')
        out = []
        for item in items:
            out.append({"id": item[0], "name": item[1]})
        return JsonResponse({"arr": out})
    else:
        return JsonResponse({"arr": [{}]})

@login_required
def items_request(request):
    current_user = request.user
    product_code = request.META['QUERY_STRING'].split("=")[1]
    product = models.Product.objects.get(productCode=product_code)
    output = []
    if request.user.is_authenticated():
        profile = models.UserProfile.objects.values_list('customerNumber').get(user=current_user)
        curr_customer = models.Customer.objects.get(customerNumber=profile[0])
        stocks = models.Stock.objects.values_list('productCode', 'dateRecord', 'quantity').filter(customerNumber=curr_customer, productCode=product).order_by('dateRecord')
        for item in stocks:
            output.append({"dateRecord": item[1], "quantity": item[2]})
            #writer.writerow([item[1], item[2]])
    return JsonResponse({"output": output})
