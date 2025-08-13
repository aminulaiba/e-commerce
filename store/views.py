from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category


from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .forms import SignUpForm

# Create your views here.

def start(request):
    return HttpResponse("Allah is the almighty!")


def home(request):
    products = Product.objects.all()
    category = Category.objects.all()
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
            return redirect(home)
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