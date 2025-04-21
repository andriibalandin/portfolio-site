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
        return GeneralProduct.objects.all().union(VinylRecord.objects.all())


class ProductDetailView(DetailView):
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        slug = self.kwargs['slug']
        general_qs = GeneralProduct.objects.filter(slug=slug)
        if general_qs.exists():
            return general_qs
        return VinylRecord.objects.filter(slug=slug)