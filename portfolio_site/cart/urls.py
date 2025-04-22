from django.urls import path
from .views import CartView, add_to_cart

app_name = 'cart'
urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<str:product_type>/<int:product_id>/', add_to_cart, name='add_to_cart')
]