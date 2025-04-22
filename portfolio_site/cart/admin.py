from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(CartItem)
class AdminCartItem(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']