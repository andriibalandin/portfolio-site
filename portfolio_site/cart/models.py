from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username if self.user else 'Guest'}"

    def get_total(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitem_set')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Unknown Product'}"

    def get_total_price(self):
        if self.product and hasattr(self.product, 'get_discounted_price'):
            return self.quantity * self.product.get_discounted_price()
        return 0
    
    def clean(self):
        if not self.product:
            raise ValidationError("Товар не існує.")
        if not self.product.is_available or self.product.quantity == 0:
            raise ValidationError(f"Товар {self.product.name} не в наявності.")
        if self.quantity > self.product.quantity:
            raise ValidationError(f"Недостатньо товару {self.product.name}. В наявності: {self.product.quantity} шт.")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        