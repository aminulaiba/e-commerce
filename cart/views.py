import json
from django.http import JsonResponse
from .cart import CartManager
from store.models import Product
from .models import Shipping, Cart
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse

from .models import Order, OrderItem


# Create your views here.

def cart(request):
    cart = CartManager(request)
    cart_items, subtotal_price =cart.cart_products()
    if request.user.is_authenticated:
        saved_addresses = Shipping.objects.filter(user=request.user)
    else:
        saved_addresses = []

    shipping = 30 if subtotal_price!=0 else 0
    total = subtotal_price+shipping
    return render(request, 'cart/cart-test.html', {'cart_products': cart_items, 'subtotal': subtotal_price, 'shipping': shipping, 'total': total, 'saved_addresses':saved_addresses})
    

def cart_add(request):
    cart = CartManager(request)
    if request.method == 'POST':
        product_id = int(json.loads(request.body).get('product_id'))
        product_qty = int(json.loads(request.body).get('qty'))

        total_cart_items = cart.add(product_id, product_qty)
        return JsonResponse({'cart': total_cart_items})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    cart = CartManager(request)
    body = request.body
    prodId = json.loads(body).get('prodId')
    # cart = SessionCart(request)
    total_cart_items, total = cart.remove(prodId)
    return JsonResponse({'cart': total_cart_items, 'total': total})
    # return JsonResponse({'redirect_url': reverse('cart')})

# for updating the quantity in cart page
def cart_update(request):
    cart = CartManager(request)
    body = json.loads(request.body)
    prodId = body.get('prodId')
    updval = int(body.get('updval'))
    total_cart_items, total = cart.update(prodId, updval)
    return JsonResponse({'cart': total_cart_items, 'total': total})



def place_order(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            shipping_address_id = request.POST.get('shipping_address')
            payment = request.POST.get('payment')
            cart = Cart.objects.filter(user=request.user, is_active=True).last()
            address = Shipping.objects.get(id=shipping_address_id, user=request.user)
            full_address = f"{address.full_name} {address.address_line_1}, {address.postal_code}, {address.city}, {address.phone}"

            cart = CartManager(request)
            cart_items, subtotal_price =cart.cart_products()
            total = subtotal_price+ 30 if subtotal_price>0 else 0

            # creating an Order object and save to DB
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                shipping_address=full_address,
                payment_method = payment
            )

            # Now create OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    unit_price=item.product.price,
                    total_price=item.quantity * item.product.price
                )
            
            # Cleaning the cart items
            cart.cart_delete()
            
            return JsonResponse({"success": True, "message": "Order placed!"})
        else:
            return JsonResponse({"success": False, "message": "Order Not placed!"})
    else:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address = request.POST.get('address')
            city = request.POST.get('city')
            zip_code = request.POST.get('zip_code')
            email = request.POST.get('email')

            # Example: print or save the data
            print("Name:", f"{first_name} {last_name}")
            print("Address:", address)
            print("City:", city)
            full_address = f"{first_name} {last_name}, {address}, {zip_code}, {city}, {email}"

            cart = CartManager(request)
            cart_items, subtotal_price =cart.cart_products()
            total = subtotal_price+ 30 if subtotal_price>0 else 0
            # You can now create an Order object and save to DB
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                total_amount=total,
                shipping_address=full_address
            )

            # Now create OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    quantity=item['quantity'],
                    unit_price=item['product'].price,
                    total_price=item['quantity'] * item['product'].price
                )
            
            # Cleaning the cart items
            cart.clear()

            return JsonResponse({"success": True, "message": "Order placed!"})
        else:
            return JsonResponse({"success": False, "message": "Order Not placed!"})
        



