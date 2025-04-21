from django.contrib import admin
from .models import Category, GeneralProduct, VinylRecord, Genre, Artist, Manufacturer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GeneralProduct)
class GeneralProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount', 'is_new']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(VinylRecord)
class VinylRecordAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount', 'is_new', 'release_year']
    prepopulated_fields = {'slug': ('name',)}
