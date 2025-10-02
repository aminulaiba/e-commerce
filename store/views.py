from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category


from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .forms import SignUpForm, UpdateUserForm, PasswordChange, UpdateProfileForm
from cart.forms import ShippingForm

# Create your views here.

def start(request):
    return HttpResponse("Allah is the almighty!")


def home(request):
    query = request.GET.get('q')
    category = Category.objects.all()
    
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'store/home.html', {'prods': products, 'category': category})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Successfull LoggedIn!:)"))
            return redirect('home')
        else:
            messages.success(request, ("Wrong user name or password!:("))
            return redirect("login")
    else:
        return render(request, 'store/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Successfully LogOut!"))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("Successfull LoggedIn!:)"))
            return redirect('update-profile')
        else:
            messages.success(request, ("Something is wrong in login!:)"))
    else:
        form = SignUpForm()
        return render(request, 'store/register.html', {'form': form})
    

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/prod-detail.html', {'product': product})

def category(request, name):
    category = Category.objects.get(name=name)
    products = Product.objects.filter(category=category)
    return render(request, 'store/home.html', {'prods': products})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = UpdateUserForm(request.POST or None, instance=current_user)
        
        profile = request.user.profile
        profile_form = UpdateProfileForm(request.POST or None, instance=profile)
        shipping_addresses = current_user.shipping_set.all()
        if request.method == "POST":
            if form.is_valid() and profile_form.is_valid():
                form.save()
                profile_form.save()
                messages.success(request, "Updated Done.")
                return redirect('home')
    context={'form':form, 'profile_form':profile_form, 'shipping_addresses':shipping_addresses}
    return render(request, 'store/update-user.html', context=context)
    

def shipping_address(request):
    form = ShippingForm()
    if request.method == "POST":
        form = ShippingForm(request.POST)
        if form.is_valid():
            shiping=form.save(commit=False)
            shiping.user = request.user
            shiping.save()
            return redirect('update-user')

    return render(request, 'store/shipping.html', {'form':form})






    
# updating the extra info about the user   
def update_profile(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        if request.method == "POST":
            form = UpdateProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile saved successfully!")
                return redirect('update-user')
        else:
            form = UpdateProfileForm(instance=profile)
    return render(request, 'store/profile-update.html', {'form': form})



    

def password_change(request):
    current_user = request.user
    if current_user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChange(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password has changed.")
            else:
                for field_errors in form.errors.values():
                    for error in field_errors:
                        messages.error(request, error)
                return redirect('password-change')
        else:
            form = PasswordChange(current_user)
    else:
        messages.success(request, "U need to login first!")
    return render(request, 'store/password-change.html', {'form': form})  
        