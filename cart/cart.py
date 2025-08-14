from store.models import Product
class Cart:
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

    # def count_items(self):
    #     return sum(item['qty'] for item in self.cart.values())



    # Calculating the subprice of an item
    def sub_price(self):
        pass


    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.save()
        total, cart_prods = self.checkout_totals()
        
        return sum(self.cart.values()), total
    
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
            dic = {'product': v, 'qty': self.cart[str(p_id)]}
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


