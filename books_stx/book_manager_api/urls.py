from django.urls import path
from book_manager_api.views import BookAPIView

urlpatterns = [
    path('books/', BookAPIView.as_view(), name='api-book-list'),
]