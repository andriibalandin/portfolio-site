import django_filters
from .models import Post, Category, Tag
from django.contrib.auth.models import User

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Назва')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Категорія')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        widget=django_filters.widgets.forms.CheckboxSelectMultiple,
        label='Теги'
    )
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Автор')

    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'author']
