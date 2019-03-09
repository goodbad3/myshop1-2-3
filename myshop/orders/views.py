from django.shortcuts import render
from .tasks import order_created
from .models import OrderItem
from .forms import OrderCreateForm

from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
#验证通过之后执行order = form.save()创建新订单对象并写入数据库

            for item in cart:

                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # 成功生成OrderItem之后清除购物车
            cart.clear()
            # 启动异步任务
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', locals())
