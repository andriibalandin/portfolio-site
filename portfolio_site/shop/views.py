from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Product, Genre
from .filters import ProductFilter

class HomeView(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_products'] = Product.objects.filter(is_new=True, category__slug='other')[:3]
        context['new_vinyl'] = Product.objects.filter(is_new=True, category__slug='vinyl-records')[:3]
        context['discounted_products'] = Product.objects.filter(discount__isnull=False, category__slug='other')[:3]
        context['discounted_vinyl'] = Product.objects.filter(discount__isnull=False, category__slug='vinyl-records')[:3]
        return context

class ProductListView(ListView):
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class ProductDetailView(DetailView):
    template_name = 'shop/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_type'] = 'vinyl' if self.object.category.slug == 'vinyl-records' else 'general'
        return context