from .cart import SessionCart
from .models import Cart as loggedUserCart

def cart(request):
    if request.user.is_authenticated and not request.user.is_staff:
        cart = loggedUserCart.objects.filter(user=request.user, is_active=True).order_by('-created_at').first()
        if not cart:
            cart = loggedUserCart.objects.create(user=request.user, is_active=True)
        
        return {
            'cart': cart,
            'prod_count': cart.cart_total_items,
        }
    else:
        cart = SessionCart(request)
        return {
            'cart': cart,
            'prod_count': sum(cart.cart.values()),
        }