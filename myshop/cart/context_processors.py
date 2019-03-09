from .cart import Cart

def cart(request):
    return {'cart': Cart(request) }

#将购物车设置到request上下文中