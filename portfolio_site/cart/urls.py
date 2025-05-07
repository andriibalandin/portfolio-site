from django.urls import path
from .views import CartView, add_to_cart, update_cart_item, remove_cart_item

app_name = 'cart'
urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
]