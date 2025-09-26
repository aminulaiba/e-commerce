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
            total, cart_prods = self.checkout_totals()
            print('total: ', total, 'pros: ', cart_prods)
            return sum(self.cart.values()), total

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            total, cart_prods = self.checkout_totals()
        return sum(self.cart.values()), total

    def cart_products(self):
        cart_products = []
        total, products = self.checkout_totals()
        for p_id, v in products.items():
            dic = {'product': v, 'price_at_time': v.sale_price if v.on_sale else v.price, 'qty': self.cart[str(p_id)]}
            cart_products.append(dic)
        return cart_products, total
    
    # Final total from DB for checkout
    def checkout_totals(self):
        cart = self.cart
        products_ids = self.cart.keys()
        total = 0
        products = Product.objects.filter(id__in=products_ids).in_bulk()

        for id, prod in products.items():
            current_price = prod.sale_price if prod.on_sale else prod.price
            sub_tot = float(current_price*cart[str(id)])
            total += sub_tot
        return total, products






#  cart from db for logged in user
class DBCart:
    def __init__(self, user):
        self.user = user
        self.cart = Cart.objects.filter(user=user, is_active=True).last()

    def cart_products(self):
        # cart_products = CartItem.objects.filter(cart=self.cart)
        cart_products = []
        # item structure is {'product': v, 'qty': self.cart[str(p_id)]}
        products = self.cart.items.all()
        for item in products:
            dic = {'product': item.product, 'price_at_time': item.price_at_time, 'qty': item.quantity}
            cart_products.append(dic)
        total = self.checkout_totals()
        return cart_products, total
    
    def checkout_totals(self):
        return sum([p.price_at_time*p.quantity for p in self.cart.items.all()])

    def total_quantity(self):
        return self.cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    def item_current_price(self, product_id):
        product = get_object_or_404(Product, id=product_id)
        return product.price if not product.on_sale else product.sale_price

    def add(self, product_id, quantity=1):
        item, created = CartItem.objects.get_or_create(
            cart=self.cart,
             product_id=product_id,
              defaults={
                  'quantity': 1,
                  'price_at_time': self.item_current_price(product_id)
                  }
            )
        if not created:
            item.quantity = item.quantity+ quantity
            item.save()

        total_quantity = self.cart.items.aggregate(total=Sum('quantity'))['total'] or 0
        return total_quantity
    
    def update(self, prodId, updval):
        print("hiii")
        cart_item = self.cart.items.get(cart=self.cart, product__id=prodId)
        cart_item.quantity = updval
        cart_item.save()
        total_quantity = self.total_quantity()
        total = self.checkout_totals()
        print(cart_item)
        return total_quantity, total

    def remove(self, product_id):
        item = self.cart.items.get(cart=self.cart, product_id=product_id)
        item.delete()
        total_quantity = self.total_quantity()
        total = self.checkout_totals()
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