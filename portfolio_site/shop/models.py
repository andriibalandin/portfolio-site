from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg
from easy_thumbnails.fields import ThumbnailerImageField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    is_new = models.BooleanField(default=False)
    image = ThumbnailerImageField(upload_to='products/', blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    release_year = models.PositiveIntegerField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    is_available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    def get_discounted_price(self):
        if self.discount:
            return round(self.price * (1 - self.discount/100), 2)
        return self.price
    
    def update_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.rating = round(avg_rating or 0.0, 1)
        self.save()


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"

    class Meta:
        unique_together = ('product', 'user')
        