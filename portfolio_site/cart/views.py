from django.forms import ValidationError
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import DetailView
from django.contrib.contenttypes.models import ContentType
from .models import Cart, CartItem
from shop.models import Product


class CartView(DetailView):
    model = Cart
    template_name = 'cart/cart.html'
    context_object_name = 'cart'

    def get_object(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            return cart
        else:
            session_cart_id = self.request.session.get('cart_id')
            if session_cart_id:
                return get_object_or_404(Cart, id=session_cart_id)
            cart = Cart.objects.create()
            self.request.session['cart_id'] = cart.id
            return cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if not product.is_available or product.quantity == 0:
        return redirect('shop:product_detail', slug=product.slug)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart = get_object_or_404(Cart, id=session_cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id

    content_type = ContentType.objects.get_for_model(Product)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        content_type=content_type,
        object_id=product.id
    )
    try:
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
    except ValidationError as e:
        if item_created:
            cart_item.delete()  
    return redirect('cart:cart')

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
    return redirect('cart:cart')

def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart:cart')