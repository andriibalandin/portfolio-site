from django.urls import path
from .views import OrderCreateView, OrderDetailView

app_name = 'orders'
urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]