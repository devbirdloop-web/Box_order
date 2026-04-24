class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product):
        pid = str(product.id)

        if pid not in self.cart:
            self.cart[pid] = {
                'name': product.name,
                'price': float(product.price),
                'qty': 1
            }
        else:
            self.cart[pid]['qty'] += 1

        self.save()

    def update(self, product, qty):
        pid = str(product.id)

        if pid in self.cart:
            self.cart[pid]['qty'] = int(qty)
            self.save()

    def remove(self, product):
        pid = str(product.id)

        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def total(self):
        return sum(item['price'] * item['qty'] for item in self.cart.values())