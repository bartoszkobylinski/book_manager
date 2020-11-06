from django.urls import path
from django_filters.views import FilterView
from book_manager.filters import BookFilter
from book_manager.views import AddBookView, GoogleApiView

urlpatterns = [
    path("", FilterView.as_view(filterset_class=BookFilter, template_name='books.html'), name="books"),
    path("add_book/", AddBookView.as_view(), name="add_book"),
    path("import_books", GoogleApiView.as_view(), name='import_books'),
]
