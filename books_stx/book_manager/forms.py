from django.forms import ModelForm
from book_manager.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['author', 'title', 'publish_year', 'isbn', 'pages', 'cover', 'language']
