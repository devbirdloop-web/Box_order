from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders, name='orders'),

    path('cart/', views.cart_view, name='cart'),

    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'), 
    path('my-orders/', views.my_orders, name='my_orders'),
]