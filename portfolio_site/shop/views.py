from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Product, Genre
from .filters import ProductFilter
from .forms import ReviewForm

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
        context['review_form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            product.update_rating()
            return redirect(product.get_absolute_url())
        context = self.get_context_data()
        context['review_form'] = form
        return self.render_to_response(context)
    