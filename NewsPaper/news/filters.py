from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter, ChoiceFilter
from django.forms.widgets import DateInput
from .models import Post, Author

class PostFilter(FilterSet):
    title__icontains = CharFilter(field_name='title', lookup_expr='icontains', label='Title (contains)')

    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор',
        to_field_name='user'  # Используйте 'username', если это поле для представления авторов в списке
    )

    created_at__gt = DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Дата создания после',  # Чтобы было понятнее, что фильтрует этот фильтр
        widget=DateInput(attrs={'type': 'date'})
    )
    # Если хотите использовать username автора в фильтре


    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'created_at': ['gt'],
        }