from django.urls import path

from carts import views
from orders.views import initiate_payment

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:artwork_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:artwork_id>/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('initiate-payment/<slug:order_number>/', initiate_payment, name='initiate_payment'),
]