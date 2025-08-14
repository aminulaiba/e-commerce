import json
from django.http import JsonResponse
from .cart import Cart
from store.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


# Create your views here.

def cart(request):
    print(dict(request.session))
    cart = Cart(request)
    cart_products, subtotal_price = cart.cart_products()
    tot=cart.checkout_totals()
    print("actual totals from db: ", tot)
    shipping = 30
    total = subtotal_price+shipping
    return render(request, 'cart/cart.html', {'cart_products': cart_products, 'subtotal': subtotal_price, 'shipping': shipping, 'total': total })

def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(json.loads(request.body).get('product_id'))
        product_qty = int(json.loads(request.body).get('qty'))

        product = get_object_or_404(Product, pk=product_id)
        total_cart_items, total = cart.add(product_id, product_qty)
        return JsonResponse({'cart': total_cart_items, 'total': total})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    body = request.body
    prodId = json.loads(body).get('prodId')
    cart = Cart(request)
    total_cart_items, total = cart.remove(prodId)
    return JsonResponse({'cart': total_cart_items, 'total': total})
    # return JsonResponse({'redirect_url': reverse('cart')})

def cart_update(request):
    cart = Cart(request)
    body = json.loads(request.body)
    prodId = body.get('prodId')
    updval = int(body.get('updval'))
    # cart.update(prodId, updval)
    total_cart_items, total = cart.update(prodId, updval)
    return JsonResponse({'cart': total_cart_items, 'total': total})

