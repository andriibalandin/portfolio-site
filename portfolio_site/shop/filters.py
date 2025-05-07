import django_filters
from django import forms
from .models import Product, Category, Genre, Artist

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Пошук за назвою',
        widget=forms.TextInput(attrs={'placeholder': 'Введіть назву'})
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категорія',
        empty_label='Усі категорії'
    )
    genre = django_filters.ModelChoiceFilter(
        queryset=Genre.objects.all(),
        label='Жанр',
        empty_label='Усі жанри'
    )
    artist = django_filters.ModelChoiceFilter(
        queryset=Artist.objects.all(),
        label='Виконавець',
        empty_label='Усі виконавці'
    )
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Мін. ціна'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Макс. ціна'
    )
    has_discount = django_filters.BooleanFilter(
        field_name='discount',
        lookup_expr='isnull',
        exclude=True,
        label='Тільки зі знижкою',
        widget=forms.CheckboxInput
    )
    rating_min = django_filters.NumberFilter(
        field_name='rating',
        lookup_expr='gte',
        label='Мін. рейтинг'
    )
    is_new = django_filters.BooleanFilter(
        field_name='is_new',
        label='Тільки новинки',
        widget=forms.CheckboxInput
    )
    sort_by = django_filters.ChoiceFilter(
        label='Сортувати',
        choices=[
            ('price_desc', 'За ціною (спадання)'),
            ('price_asc', 'За ціною (зростання)'),
            ('rating_desc', 'За рейтингом (спадання)'),
            ('rating_asc', 'За рейтингом (зростання)'),
        ],
        method='filter_sort_by',
        empty_label='Без сортування'
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'genre', 'artist', 'price_min', 'price_max', 'has_discount', 'rating_min', 'is_new', 'sort_by']

    def filter_sort_by(self, queryset, name, value):
        print(f"Sort by: {value}")
        if value == 'price_desc':
            return queryset.order_by('-price')
        elif value == 'price_asc':
            return queryset.order_by('price')
        elif value == 'rating_desc':
            return queryset.order_by('-rating')
        elif value == 'rating_asc':
            return queryset.order_by('rating')
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.form.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput)):
                field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select select2'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})