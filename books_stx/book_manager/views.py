from django.views.generic import ListView, CreateView, FormView
from django.shortcuts import redirect
from book_manager.forms import BookForm, GoogleApiForm
from book_manager.models import Book
from book_manager.google_book_api import GoogleAPIParser
from book_manager.CONSTANS import GOOGLE_API_KEY

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


class GoogleApiView(FormView):
    form_class = GoogleApiForm
    template_name = "import_google.html"
    success_url = "books"
    '''
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title', '')
        author = cleaned_data.get('author', '')
        publisher = cleaned_data.get('publisher', '')
        subject = cleaned_data.get('subject', '')
        isbn = cleaned_data.get('isbn', '')
        lccn = cleaned_data.get('lccn', '')
        oclc = cleaned_data.get('oclc', '')
    '''    
    def form_valid(self, form):
        user_kwargs = {}
        user_kwargs.update(title=form.cleaned_data['title'])
        user_kwargs.update(author=form.cleaned_data['authors'])
        user_kwargs.update(subject=form.cleaned_data['subject'])
        user_kwargs.update(isbn_10=form.cleaned_data['isbn_number'])
        user_kwargs.update(lccn_number=form.cleaned_data['lccn_number'])
        user_kwargs.update(oclc_number=form.cleaned_data['oclc_number'])
        if user_kwargs:
            user_query = GoogleAPIParser(GOOGLE_API_KEY, **user_kwargs)
            user_query.save_books_to_database()
            return redirect('books')
        else:
            return redirect('books')

