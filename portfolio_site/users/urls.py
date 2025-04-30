from django.urls import path
from .views import CustomLoginView, ProfileView, RegsterView
from django.contrib.auth.views import LogoutView

app_name = 'users'
urlpatterns = [
    path('register/', RegsterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]