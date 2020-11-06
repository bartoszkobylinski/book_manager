from django.urls import path
from book_manager.views import BookListView, AddBookView, GoogleApiView

urlpatterns = [
    path("books/", BookListView.as_view(), name="books"),
    path("add_book/", AddBookView.as_view(), name="add_book"),
    path("import_books", GoogleApiView.as_view(), name='import_books'),
]
