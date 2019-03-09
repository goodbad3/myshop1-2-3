from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    """
    当一个订单创建完成后发送邮件通知给用户
    """
    order = Order.objects.get(id=order_id)
    subject = '订单号. {}'.format(order.id)
    message = '尊敬的 {},\n\n您已成功下订单。您的订单号是  {}.'.format(order.name,
                                                                             order.id)
    mail_sent = send_mail(subject, message, '573908896@qq.com', [order.email])
    return mail_sent
