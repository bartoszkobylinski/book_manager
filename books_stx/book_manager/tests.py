from django.test import TestCase
from book_manager.models import Book

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TestDjangoInstallation(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_if_django_is_instaled_and_runs(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000")
        browser = driver
        self.assertIn("Django", browser.title)


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
