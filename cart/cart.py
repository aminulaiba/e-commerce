from store.models import Product
from .models import Cart, CartItem

from django.db.models import Sum
from django.shortcuts import get_object_or_404


#  cart from session for annonymous user
class SessionCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart
        self.old_cart = [] # to keep old items of the cart. to avaid extra db calls for total price when update a item


    def save(self):
        # Optional: explicitly mark the session as modified
        self.session.modified = True

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.save()
        return sum(self.cart.values())
    
    def update(self, prodId, updval):
        if prodId in self.cart:
            self.cart[prodId] = updval
            self.save()

            total = self.checkout_totals()
            print('total: ', total)
            return sum(self.cart.values()), total

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            total = self.checkout_totals()
        return sum(self.cart.values()), total

    def cart_products(self):
        products_ids = self.cart.keys()
        cart_products = Product.objects.filter(id__in=products_ids)

        products_list = []
        for item in cart_products:
            # this structure would mimic the queryset with .select_related() that used for loggedin user 
            # so that the same template can handle both for annonymous and loged user.
            dic = {'product': item, 'quantity': self.cart[str(item.id)]} 
            products_list.append(dic)

        subtotal = self.checkout_totals()
        return products_list, subtotal
    
    # Final total from DB for checkout
    def checkout_totals(self):
        cart = self.cart
        total = 0

        products_ids = self.cart.keys()
        cart_products = Product.objects.filter(id__in=products_ids)
    
        for prod in cart_products:
            current_price = prod.sale_price if prod.on_sale else prod.price
            sub_tot = float(current_price*cart[str(prod.id)])
            total += sub_tot
        return total






#  cart from db for logged in user
class DBCart:
    def __init__(self, user):
        self.user = user
        self.cart = Cart.objects.filter(user=user, is_active=True).last()

    # im not using this property coz if i use it in the checkout_total method directly then it need to be called twich in the cart view.
    # one for having all the product and another for the total itself. but now im calling the db once and then passing it as arg in the
    # check_total
    # @property
    # def cart_items(self):
    #     return self.cart.items.select_related("product")

    def cart_products(self):
        cart_items = self.cart.items.select_related("product")
        total = self.checkout_totals(cart_items)
        print(total)
        return cart_items, total
    
    def checkout_totals(self, cart_items):
        return sum((p.product.sale_price if p.product.on_sale else p.product.price) * p.quantity for p in cart_items)

    def total_quantity(self):
        return self.cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    def add(self, product_id, quantity=1):
        item, created = CartItem.objects.get_or_create(
            cart=self.cart,
             product_id=product_id,
              defaults={
                  'quantity': quantity,
                  }
            )
        if not created:
            item.quantity = item.quantity+ quantity
            item.save()
        total_quantity = self.cart.items.aggregate(total=Sum('quantity'))['total'] or 0
        return total_quantity
    
    def update(self, prodId, updval):
        cart_item = self.cart.items.get(cart=self.cart, product__id=prodId)
        cart_item.quantity = updval
        cart_item.save()
        cart_items = self.cart.items.select_related("product")
        total_quantity = self.total_quantity()
        total = self.checkout_totals(cart_items)

        return total_quantity, total

    def remove(self, product_id):
        item = self.cart.items.get(cart=self.cart, product_id=product_id)
        item.delete()
        total_quantity = self.total_quantity()
        cart_items = self.cart.items.select_related("product")

        total = self.checkout_totals(cart_items)
        return total_quantity, total



#  cart manager that switches between sessio and db
class CartManager:
    def __init__(self, request):
        self.request = request
        if request.user.is_authenticated:
            self.cart = DBCart(request.user)
        else:
            self.cart = SessionCart(request)

    def __getattr__(self, name):
        return getattr(self.cart, name)