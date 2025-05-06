from django.urls import path
from .views import CustomLoginView, ProfileView, RegisterView, FollowAuthorView, UnfollowAuthorView
from django.contrib.auth.views import LogoutView

app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('subscribe/', ProfileView.as_view(), name='subscribe'),
    path('follow/<int:user_id>/', FollowAuthorView.as_view(), name='follow_author'),
    path('unfollow/<int:user_id>/', UnfollowAuthorView.as_view(), name='unfollow_author'),
]