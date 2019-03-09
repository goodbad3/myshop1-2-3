from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:

    def __init__(self, request):
        #初始化购物车对象
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)


        if not cart:
            #向session中存入空白购物车数据
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self): 
        """
        购物车内一共有几种商品
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        遍历所有购物车中的商品并从数据库中取得商品对象
        """
        product_ids = self.cart.keys()
        # 获取购物车内的所有商品对象
        #获取了当前购物车中所有商品的Product对象。然后浅拷贝了一份cart购物车数据，
        #-->>并为其中的每个商品添加了键为product
##{'id键':{"数量":"xx", "price":"xx", "product":"xx"},  ...}
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            #item中没有id键，产出{"数量":"xx", "price":"xx", "product":"xx",'total_price':"xxx"}
##{ 'id键':{"数量":"xx", "price":"xx", "product":"xx",'total_price':"xxx"},   ...}

    def add(self, product, quantity=1, update_quantity=False):

   # 向购物车中增加商品或者更新购物车中的数量

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:

            self.cart[product_id]['quantity'] += quantity
        self.save()
##{'id键':{"数量":"xx", "price":"xx"}, ...}

    def remove(self, product):
        """
        从购物车中删除商品
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
    # 设置session.modified的值为True，中间件在看到这个属性的时候，就会保存session
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):

        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
