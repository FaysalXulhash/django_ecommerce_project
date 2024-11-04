from django.urls import path
from .views import cart, add_cart, remove_cart, remove_cart_item

urlpatterns = [
    path('', cart, name='cart'),
    path('add-cart/<int:product_id>/', add_cart, name='add-cart'),
    path('remove-cart/<int:product_id>/<int:cart_item_id>/', remove_cart, name='remove-cart'),
    path('remove-cart-item/<int:product_id>/<int:cart_item_id>/', remove_cart_item, name='remove-cart-item'),

]
