from django.urls import path
from book_manager.views import BookListView

urlpatterns = [
    path("books/", BookListView.as_view(), name="books"),
]
