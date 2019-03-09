from django.urls import path, re_path

from . import views
app_name = "cart"

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('cart-add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart-remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
