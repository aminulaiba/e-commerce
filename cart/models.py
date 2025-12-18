from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import pre_save
import uuid
import datetime

from store.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)    
    
    @property
    def cart_total(self):
        return sum(item.total_price for item in self.items())
    
    @property
    def cart_total_items(self):
        return self.items.aggregate(total=Sum('quantity'))['total'] or 0
    
    def __str__(self):
        return f"Cart {self.id} ({self.user or 'Guest'})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    # price_at_time = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of adding
    is_selected = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_price(self):
        return self.quantity * self.price_at_time
    
    def __str__(self):
        return f"Cart {self.id} ({self.product.name}) {self.cart.user}"



def generate_order_number():
    return uuid.uuid4().hex[:12].upper()
class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending Payment'),
        ('processing', 'Processing'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    ORDER_DELIVERY_STATUS = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    delivery_status = models.CharField(max_length=20, choices=ORDER_DELIVERY_STATUS, default='processing', db_index=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    # billing_address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, default='cod')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        # return f"Order #{self.order_number} - {self.user.username}"
        user_part = self.user.username if self.user else "Unknown User"
        return f"Order #{self.order_number} - {user_part}"
    
@receiver(pre_save, sender=Order)
def delivered_date_set(sender, instance, **kwarg):
    if instance.pk:
        old_obj = sender.objects.get(pk=instance.pk)
        if instance.delivery_status == "delivered" and old_obj.delivery_status != "delivered": # old obj needs to be checked coz otherwise it will get updated each time with any updation of unrelated fields.
            instance.delivery_date = datetime.datetime.now()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=255)  # Snapshot of product name at time of purchase
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of purchase
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name} (Order #{self.order.order_number})"
    



class Shipping(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100) # receiver full name
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=225)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"id: {self.id} {self.full_name} ({self.phone}) -- {self.address_line_1}"
    