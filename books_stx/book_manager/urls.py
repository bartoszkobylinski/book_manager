from django.urls import path
from book_manager.views import BookListView, AddBookView

urlpatterns = [
    path("books/", BookListView.as_view(), name="books"),
    path("add_book/", AddBookView.as_view(), name="add_book"),
]
