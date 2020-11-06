import django_filters
from book_manager.models import Book


class BookFilter(django_filters.FilterSet):
    authors = django_filters.CharFilter(lookup_expr="icontains", field_name='authors')
    title = django_filters.CharFilter(lookup_expr="icontains", field_name="title")
    language = django_filters.CharFilter(lookup_expr="icontains", field_name="language")
    publish_year__gt = django_filters.NumberFilter(field_name="publish_year", lookup_expr="gt")
    publish_year__lt = django_filters.NumberFilter(field_name="publish_year", lookup_expr="lt")

    class Meta:
        model = Book
        fields = ['authors', 'title', 'language', 'publish_year']
