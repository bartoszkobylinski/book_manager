from django.views.generic import CreateView, FormView, UpdateView
from django.shortcuts import redirect
from book_manager.forms import GoogleApiForm
from book_manager.models import Book
from book_manager.google_book_api import GoogleAPIParser
from book_manager.CONSTANS import GOOGLE_API_KEY


class AddBookView(CreateView):
    model = Book
    fields = ['authors',
              'title',
              'publish_year',
              'isbn_10',
              'isbn_13',
              'oclc_number',
              'lccn_number',
              'pages',
              'language',
              'subject',
              'cover']
    template_name = "book_manager/add_book.html"


class UpdateBookView(UpdateView):
    model = Book
    fields = ['authors',
              'title',
              'publish_year',
              'isbn_10',
              'isbn_13',
              'oclc_number',
              'lccn_number',
              'pages',
              'language',
              'cover']
    template_name = 'book_manager/update-book.html'


class GoogleApiView(FormView):
    form_class = GoogleApiForm
    template_name = "book_manager/import_google.html"
    success_url = "books"

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
