from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username




class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'


from django.contrib.auth.hashers import make_password
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.first_name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    
    # adding sale stuff
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} --> {self.customer}"
