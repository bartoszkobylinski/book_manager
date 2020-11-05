from django.views.generic import ListView, CreateView
from book_manager.forms import BookForm
from book_manager.models import Book

# Create your views here.


class BookListView(ListView):
    model = Book
    template_name = "books.html"

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset
    


class AddBookView(CreateView):
    form_class = BookForm
    template_name = "add_book.html"
