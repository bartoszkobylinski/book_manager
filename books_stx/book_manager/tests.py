from django.test import TestCase, Client
from django.urls import reverse
from book_manager.models import Book
from book_manager.views import BookListView


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TestDjangoInstallation(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_if_django_is_instaled_and_runs(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/books")
        browser = driver
        self.assertIn("Django books", browser.title)


class TestBookMode(TestCase):

    def test_retrieving_and_saving_book_model(self):
        book = Book(
            author='Author',
            title="Title",
            publish_year=1520,
            isbn='123456780123',
            pages=152,
            cover='http:/eueu',
            language="pl")
        book.save()
        books_query = Book.objects.all()
        self.assertEqual(books_query.count(), 1)


class TestBookListView(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('books'))

    def test_book_list_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_book_list_view_is_using_correct_template(self):
        self.assertTemplateUsed(self.response, 'books.html')
