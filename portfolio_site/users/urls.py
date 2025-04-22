from django.urls import path
from .views import CustomLoginView, CustomLogoutView, ProfileView

app_name = 'users'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]