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
        return sum(self.cart.values())
    
    def update(self, prodId, updval):
        if prodId in self.cart:
            self.cart[prodId] = updval
            self.save()
            return sum(self.cart.values())
        else:
            return "prod id isnt in the session"

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
        return sum(self.cart.values())

    def cart_products(self):
        productList = self.cart.keys()
        cart_products = []
        total = 0
        for i in productList:
            product = Product.objects.get(id=i)
            if product.on_sale:
                sub_total = product.sale_price * self.cart[i]
            else:
                sub_total = product.price * self.cart[i]

            total += sub_total

            dic = {'product': product, 'qty': self.cart[i], 'sub_total': sub_total}
            cart_products.append(dic)

        # cart_products = Product.objects.filter(id__in=productList)

        return cart_products, total


