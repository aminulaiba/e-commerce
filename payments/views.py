from django.shortcuts import render
from cart.cart import CartManager

# Create your views here.
def order_details(request):
    cart = CartManager(request)
    cart_items, subtotal_price =cart.cart_products()

    shipping = 30 if subtotal_price!=0 else 0
    total = subtotal_price+shipping
    return render(request, 'payments/checkout.html', {'cart_products': cart_items, 'subtotal': subtotal_price, 'shipping': shipping, 'total': total})
    
