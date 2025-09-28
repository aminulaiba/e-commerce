import json
from django.http import JsonResponse
from .cart import SessionCart, DBCart, CartManager
from store.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


# Create your views here.

def cart(request):
    cart = CartManager(request)
    cart_items, subtotal_price =cart.cart_products()

    shipping = 30 if subtotal_price!=0 else 0
    total = subtotal_price+shipping
    return render(request, 'cart/cart.html', {'cart_products': cart_items, 'subtotal': subtotal_price, 'shipping': shipping, 'total': total})
    

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

