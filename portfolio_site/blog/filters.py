import django_filters
from django import forms
from .models import Post, Category, Tag
from django.contrib.auth.models import User

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Пошук за назвою')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Категорія')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Теги'
    )
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Автор')
    followed_authors = django_filters.BooleanFilter(
        method='filter_followed_authors',
        label='Показувати пости',
        widget=forms.RadioSelect(choices=[
            (True, 'Тільки від відстежуваних авторів'),
            (False, 'Від усіх авторів'),
        ])
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'author', 'followed_authors']

    def filter_followed_authors(self, queryset, name, value):
        if value and self.request and self.request.user.is_authenticated:
            try:
                followed_profiles = self.request.user.userprofile.followed_authors.all()
                followed_users = User.objects.filter(userprofile__in=followed_profiles)
                return queryset.filter(author__in=followed_users)
            except AttributeError:
                return queryset.none()
        return queryset