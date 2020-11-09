from book_manager.filters import BookFilter
from book_manager.models import Book
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from book_manager_api.serializers import BookSerializer


class BookAPIView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["authors", "publish_year"]
    filterset_class = BookFilter
