from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail')
]
