import django_filters
from django import forms
from .models import Product, Category, Genre, Artist, Manufacturer

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
    genre = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        label='Жанр',
        conjoined=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2',
            'data-allow-clear': 'true',
            'data-placeholder': 'Пошук жанрів'
        })
    )
    artist = django_filters.ModelChoiceFilter(
        queryset=Artist.objects.all(),
        label='Виконавець',
        empty_label='Усі виконавці'
    )
    manufacturer = django_filters.ModelChoiceFilter(
        queryset=Manufacturer.objects.all(),
        label='Виробник',
        empty_label='Усі виробники'
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
        method='filter_has_discount',
        label='Тільки зі знижкою',
        widget=forms.CheckboxInput
    )
    rating_min = django_filters.NumberFilter(
        field_name='rating',
        lookup_expr='gte',
        label='Мін. рейтинг'
    )
    is_new = django_filters.ChoiceFilter(
        field_name='is_new',
        label='Новинки',
        choices=[
            ('true', 'Тільки новинки'),
            ('false', 'Без новинок'),
        ],
        method='filter_is_new',
        empty_label='Всі товари'
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
        fields = ['name', 'category', 'genre', 'artist', 'price_min', 'price_max', 'has_discount', 'rating_min', 'is_new', 'sort_by', 'manufacturer']

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

    def filter_has_discount(self, queryset, name, value):
        if value:
            return queryset.filter(discount__isnull=False, discount__gt=0)
        return queryset
    
    def filter_is_new(self, queryset, name, value):
        print(f"Filtering is_new with value: {value}, raw value: {self.data.get('is_new')}")
        if value == 'true':
            return queryset.filter(is_new=True)
        elif value == 'false':
            return queryset.filter(is_new=False)
        return queryset.filter(is_new=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.form.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput)):
                field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})
            elif isinstance(field.widget, forms.Select):
                if field_name in ['genre', 'artist', 'category', 'manufacturer']: 
                    field.widget.attrs.update({
                        'class': 'form-select select2',
                        'data-allow-clear': 'true',
                        'data-placeholder': field.label
                    })
                else:
                    field.widget.attrs.update({'class': 'form-select'})  
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})