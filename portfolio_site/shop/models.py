from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


def get_default_vinyl_category():
    return Category.objects.get(slug='vinyl-records').id


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
    descriprion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class BaseProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False)
    rating = models.FloatField(default=0.0)
    is_new = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])
    
    def get_discounted_price(self):
        if self.discount:
            return round(self.price * (1 - self.discount/100), 2)
        return self.price
    
    def is_vinyl_record(self):
        return isinstance(self, VinylRecord)


class GeneralProduct(BaseProduct):
    pass


class VinylRecord(BaseProduct):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_year = models.PositiveIntegerField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=get_default_vinyl_category)