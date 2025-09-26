from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile, Product
from cart.models import Cart, CartItem


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()




@receiver(user_logged_in)
def merge_cart(sender, request, user, **kwargs):
    # for the stuff or admin user no need to marge cart
    if user.is_staff or user.is_superuser:
        return
    
    # anonymous user's cart 
    session_cart = request.session.get('cart')
    if not session_cart:
        return
    
    # getting or creating the cart for the logedin user
    cart, created = Cart.objects.get_or_create(user=user)
        
    for prodId, quantity in session_cart.items():
        try:
            product = Product.objects.get(id=prodId)
        except Product.DoesNotExist:
            continue

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity':quantity,
                'price_at_time': product.sale_price if product.on_sale else product.price
            }
        )

        if not created:
            cart_item.quantity+=quantity
            cart_item.save()

    request.session['cart']={}
    request.session.modified = True