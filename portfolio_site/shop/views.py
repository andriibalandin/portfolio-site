from django.http import Http404
from django.shortcuts import render
from .models import Category, GeneralProduct, VinylRecord, Genre
from django.views.generic import TemplateView, ListView, DetailView


class HomeView(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_products'] = GeneralProduct.objects.filter(is_new=True)[:3] #мабуть додати ще фільтр для жанрів
        context['new_vinyl'] = VinylRecord.objects.filter(is_new=True)[:3]
        context['discounted_products'] = GeneralProduct.objects.filter(discount__isnull=False)[:3]
        context['discounted_vinyl'] = VinylRecord.objects.filter(discount__isnull=False)[:3]
        return context
    

class ProductListView(ListView):
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        general_products = GeneralProduct.objects.all()
        vinyl_records = VinylRecord.objects.all()
        return list(general_products) + list(vinyl_records)


class ProductDetailView(DetailView):
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        try:
            product = GeneralProduct.objects.get(slug=slug)
            self.product_type = 'general'
            return product
        except GeneralProduct.DoesNotExist:
            try:
                product = VinylRecord.objects.get(slug=slug)
                self.product_type = 'vinyl'
                return product
            except VinylRecord.DoesNotExist:
                raise Http404("Продукт не знайдено")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_type'] = self.product_type
        context['is_vinyl_record'] = self.product_type == 'vinyl'
        return context