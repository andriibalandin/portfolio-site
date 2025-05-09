import django_filters
from django import forms
from .models import Post, Category, Tag
from django.contrib.auth.models import User
from django.db.models import Count

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Пошук за назвою')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Категорія', empty_label='Усі категорії')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2',
            'data-allow-clear': 'true',
            'data-placeholder': 'Пошук тегів'
        }),
        label='Теги',
        conjoined=False
    )
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Автор', empty_label='Усі автори')
    followed_authors = django_filters.BooleanFilter(
        method='filter_followed_authors',
        label='Показувати пости',
        widget=forms.RadioSelect(choices=[
            (True, 'Тільки від відстежуваних авторів'),
            (False, 'Від усіх авторів'),
        ])
    )
    sort_by_likes = django_filters.ChoiceFilter(
        label='Сортувати за лайками',
        choices=[
            ('likes_desc', 'За спаданням'),
            ('likes_asc', 'За зростанням'),
        ],
        method='filter_sort_by_likes',
        empty_label='Без сортування'
    )
    sort_by_date = django_filters.ChoiceFilter(
        label='Сортувати за датою',
        choices=[
            ('date_desc', 'Від новіших'),
            ('date_asc', 'Від старіших'),
        ],
        method='filter_sort_by_date',
        empty_label='Без сортування'
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'author', 'followed_authors', 'sort_by_likes', 'sort_by_date']

    def filter_followed_authors(self, queryset, name, value):
        if value and self.request and self.request.user.is_authenticated:
            try:
                followed_profiles = self.request.user.userprofile.followed_authors.all()
                followed_users = User.objects.filter(userprofile__in=followed_profiles)
                return queryset.filter(author__in=followed_users)
            except AttributeError:
                return queryset.none()
        return queryset

    def filter_sort_by_likes(self, queryset, name, value):
        if value == 'likes_desc':
            return queryset.annotate(like_count=Count('likes')).order_by('-like_count')
        elif value == 'likes_asc':
            return queryset.annotate(like_count=Count('likes')).order_by('like_count')
        return queryset

    def filter_sort_by_date(self, queryset, name, value):
        if value == 'date_desc':
            return queryset.order_by('-created_at')
        elif value == 'date_asc':
            return queryset.order_by('created_at')
        return queryset
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.form.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput)):
                field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})
            elif isinstance(field.widget, forms.Select):
                if field_name in ['category', 'author', 'tags']: 
                    field.widget.attrs.update({
                        'class': 'form-select select2',
                        'data-allow-clear': 'true',
                        'data-placeholder': field.label
                    })
                else:
                    field.widget.attrs.update({'class': 'form-select'})  
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})