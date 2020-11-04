from django.views.generic import ListView
from book_manager.models import Book

# Create your views here.


class BookListView(ListView):
    model = Book
    template_name = 'books.html'

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset
