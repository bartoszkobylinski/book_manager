from django.test import TestCase, Client
from django.urls import reverse
from book_manager.models import Book
from book_manager.forms import BookForm
from django.core.exceptions import ValidationError
from book_manager.languages import get_language_codes


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


class TestBookModel(TestCase):

    def setUp(self):
        self.form = BookForm(data={
            'author': "Jhon Doe",
            'title': "Django Cook Book",
            'publish_year': 1254,
            'isbn': "1234567890153",
            'pages': 1254,
            'cover': 'http://www.camy.pl',
            'language': 'pl'
        })

    def test_retrieving_and_saving_book_model(self):
        Book.objects.create(
            author='Author',
            title="Title",
            publish_year=1520,
            isbn='12345678023',
            pages=152,
            cover='http:/eueu',
            language="pl")
        books_query = Book.objects.all()
        self.assertEqual(books_query.count(), 1)

    def test_assert_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            book = Book(
                author='Author',
                title="Title",
                publish_year=1520,
                isbn='1234567890',
                pages=152,
                cover='http:/eueu',
                language="pl")
            book.full_clean()

    def test_book_form_is_valid_with_correct_data(self):
        self.assertTrue(self.form.is_valid())

    def test_book_form_is_not_valid_with_wrong_data(self):
        self.assertFalse(self.form.is_valid())


class TestBookListView(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('books'))

    def test_book_list_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_book_list_view_is_using_correct_template(self):
        self.assertTemplateUsed(self.response, 'books.html')


class TestAddBookView(TestCase):

    def setUp(self):
        self.client = Client()
        self.add_book_url = reverse('add_book')
        self.response = self.client.get(self.add_book_url)

    def test_response_add_book_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_add_book_view_is_using_correct_template(self):
        self.assertTemplateUsed(self.response, 'add_book.html')

    def test_add_book_view_POST_method(self):

        self.client.post(
            self.add_book_url, {
                'author': "Jhon Doe",
                'title': "Django Cook Book",
                'publish_year': 1254,
                'isbn': "1234567890153",
                'pages': 1254,
                'cover': 'http://www.camy.pl',
                'language': 'pl'})
        self.assertEqual(Book.objects.last().title, "Django Cook Book")


class TestLanguagesCode(TestCase):

    def test_if_get_language_codes(self):
        language_codes = get_language_codes()
        self.assertIsInstance(language_codes, list)

    def test_if_first_element_is_removed(self):
        language_codes = get_language_codes()
        self.assertNotIn("", language_codes)
