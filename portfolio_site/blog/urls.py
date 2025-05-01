from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('post-create/', PostCreateView.as_view(), name='post-create'),
    path('post-update/<slug:slug>/', PostUpdateView.as_view(), name='post-update'),
    path('post-delete/<slug:slug>/', PostDeleteView.as_view(), name='post-delete'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),

]