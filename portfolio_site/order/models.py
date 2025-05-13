from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from shop.models import Product
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.first_name} {self.last_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitem_set', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Unknown Product'}"

    def get_cost(self):
        return self.price * self.quantity
    
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
    