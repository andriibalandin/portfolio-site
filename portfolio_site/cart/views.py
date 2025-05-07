from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView
from .models import Cart, CartItem
from shop.models import Product
from django.contrib.contenttypes.models import ContentType


class CartView(DetailView):
    model = Cart
    template_name = 'cart/cart.html'
    context_object_name = 'cart'

    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)

def add_to_cart(request, product_id, product_type):
    if product_type == 'general':
        product = get_object_or_404(Product, id=product_id)
    elif product_type == 'vinyl':
        product = get_object_or_404(Product, id=product_id)
    else:
        raise ValueError("Невідомий тип продукту")
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    content_type = ContentType.objects.get_for_model(product)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        content_type=content_type,
        object_id=product.id
    )
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart')
